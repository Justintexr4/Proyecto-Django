def quicksort(recursos, key):
    if len(recursos) <= 1:
        return recursos
    pivot = recursos[len(recursos) // 2]
    left = [x for x in recursos if x[key] < pivot[key]]
    middle = [x for x in recursos if x[key] == pivot[key]]
    right = [x for x in recursos if x[key] > pivot[key]]
    return quicksort(left, key) + middle + quicksort(right, key)

def buscar_recurso(recursos, id_recurso):
    # Implementar búsqueda binaria
    recursos_ordenados = sorted(recursos, key=lambda x: x['id'])
    low = 0
    high = len(recursos_ordenados) - 1
    while low <= high:
        mid = (low + high) // 2
        if recursos_ordenados[mid]['id'] == id_recurso:
            return recursos_ordenados[mid]
        elif recursos_ordenados[mid]['id'] < id_recurso:
            low = mid + 1
        else:
            high = mid