def normalize_path_params(cidade=None,
                         estrelas_min=0,
                         estrelas_max=5,
                         diaria_min=0,
                         diaria_max=10000,
                         limit = 50,
                         offset = 0, **dados):
    result = {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diarias_min': diaria_min,
            'diarias_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset
        }

    if not cidade: 
    #caso não haja cidade, é removida sem alterar a ordem dos demais parametros
        copy = dict(result)
        del copy['cidade']
        result = copy

    return result

consulta_padrao = "SELECT * FROM \
                    Hotel \
            WHERE (estrelas >= ? and estrelas <= ?)\
                    and (diaria >= ? and diaria <= ?)\
            LIMIT ? \
            OFFSET ? "
    
consulta_cidade = "SELECT * FROM \
                    Hotel \
            WHERE (estrelas >= ? and estrelas <= ?)\
                    and (diaria >= ? and diaria <= ?)\
                    and cidade = ? \
            LIMIT ? \
            OFFSET ? "