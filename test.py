commands = {
    '/vociao': {
        'Devuelve el mensaje en mayusculas.': '/vociao [mensaje]',
    },
    '/saved': {
        'Muestra los mensajes guardados.': '/saved y ya.'
    },
    '/spotify': {
        'Trae el link de spotify de la cancion indicada y un preview de 30 segundos (si existe).': '/spotify [cancion]'
    },
    '/ayuda': {
        'Muestra los comandos y mensajes que se pueden utilizar.': '/ayuda y ya.'
    }
}

message = ''
for k in sorted(commands):
    message += '%s: ' % k
    for k2, i in commands[k].items():
        message += '%s\nEjemplo: _%s_\n\n' % (k2, i)
# print(message)