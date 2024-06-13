from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import MetaData, select, insert, update, delete, or_, and_
from sqlalchemy.exc import SQLAlchemyError

def crea_rutas(app, db_session):
    metadata = MetaData()
    metadata.reflect(bind=db_session.bind)

    for table_name, table in metadata.tables.items():
        
        blueprint = Blueprint(f'{table_name}_crud', __name__, template_folder='templates')

        @blueprint.route('/<table_name>', methods=['GET'])
        def ver_tablas(table_name):
            try:
                table = metadata.tables[table_name]
                primary_key_column = list(table.primary_key.columns)[0].name
                
                filters = {
                    column: request.args.get(column)
                    for column in table.columns.keys()
                    if request.args.get(column)
                }
                search_term = request.args.get('search_query', default=None)
                
                query = select(table.columns)
                if search_term:
                    search_clauses = or_(
                        *[table.columns[column].ilike(f'%{search_term}%')
                        for column in table.columns.keys()]
                    )
                    query = query.where(search_clauses)
                
                if filters:
                    filter_clauses = [
                        table.columns[column].ilike(f'%{filters[column]}%')
                        for column in filters
                    ]
                    query = query.where(and_(*filter_clauses))
                
                result = db_session.execute(query).fetchall()
                columns = table.columns.keys()
                rows = [dict(row._mapping) for row in result]
                return render_template(
                    'table.html', 
                    table_name=table_name, 
                    columns=columns, 
                    rows=rows,
                    primary_key_column=primary_key_column, 
                    search_term=search_term, 
                    filters=filters
                )
            except SQLAlchemyError as e:
                db_session.rollback()
                return str(e), 500

        @blueprint.route('/<table_name>/search', methods=['GET'])
        def buscar(table_name):
            try:
                table = metadata.tables[table_name]
                primary_key_column = list(table.primary_key.columns)[0].name
                
                filters = {
                    column: request.args.get(column)
                    for column in table.columns.keys()
                    if request.args.get(column)
                }
                search_term = request.args.get('search_query', default=None)
                
                query = select(table.columns)
                if search_term:
                    search_clauses = or_(
                        *[table.columns[column].ilike(f'%{search_term}%')
                        for column in table.columns.keys()]
                    )
                    query = query.where(search_clauses)
                
                if filters:
                    filter_clauses = [
                        table.columns[column].ilike(f'%{filters[column]}%')
                        for column in filters
                    ]
                    query = query.where(and_(*filter_clauses))
                
                result = db_session.execute(query).fetchall()
                columns = table.columns.keys()
                rows = [dict(row._mapping) for row in result]
                return render_template(
                    'table.html', 
                    table_name=table_name, 
                    columns=columns, 
                    rows=rows,
                    primary_key_column=primary_key_column, 
                    search_term=search_term, 
                    filters=filters
                )
            except SQLAlchemyError as e:
                db_session.rollback()
                return str(e), 500

        @blueprint.route('/add', methods=['GET', 'POST'])
        def aniadir():
            try:
                table_name = request.args.get('table_name')
                table = metadata.tables[table_name]
                if request.method == 'POST':
                    data = {
                        column.name: request.form[column.name]
                        for column in table.columns
                        if column.name in request.form
                    }
                    query = insert(table).values(data)
                    db_session.execute(query)
                    db_session.commit()
                    return redirect(url_for(f'{table_name}_crud.ver_tablas', table_name=table_name))
                return render_template(
                    'form.html', 
                    table_name=table_name, 
                    fields=table.columns.keys(),
                    form_action=url_for('.aniadir', table_name=table_name)
                )
            except SQLAlchemyError as e:
                db_session.rollback()
                return str(e), 500

        @blueprint.route('/edit/<id>', methods=['GET', 'POST'])
        def editar(id):
            try:
                table_name = request.args.get('table_name')
                table = metadata.tables[table_name]
                primary_key_column = list(table.primary_key.columns)[0].name

                if request.method == 'POST':
                    data = {
                        column.name: request.form[column.name]
                        for column in table.columns
                        if column.name in request.form
                    }
                    query = (
                        update(table)
                        .where(table.c[primary_key_column] == id)
                        .values(data)
                    )
                    db_session.execute(query)
                    db_session.commit()
                    return redirect(url_for(f'{table_name}_crud.ver_tablas', table_name=table_name))
                else:
                    query = select(table).where(table.c[primary_key_column] == id)
                    result = db_session.execute(query).fetchone()
                    if result:
                        record = dict(result._mapping)
                        return render_template(
                            'form.html', 
                            table_name=table_name, 
                            fields=table.columns.keys(),
                            record=record, 
                            form_action=url_for(f'.editar', id=id, table_name=table_name)
                        )
                    else:
                        return "No encontrado", 404
            except SQLAlchemyError as e:
                db_session.rollback()
                return str(e), 500

        @blueprint.route('/delete/<id>', methods=['POST'])
        def eliminar(id):
            try:
                table_name = request.args.get('table_name')
                table = metadata.tables[table_name]
                primary_key_column = list(table.primary_key.columns)[0].name
                query = delete(table).where(table.c[primary_key_column] == id)
                result = db_session.execute(query)
                db_session.commit()
                return redirect(url_for(f'{table_name}_crud.ver_tablas', table_name=table_name))
            except SQLAlchemyError as e:
                db_session.rollback()
                return str(e), 500

        app.register_blueprint(blueprint, url_prefix=f'/{table_name}')
