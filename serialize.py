""" Using this file to serialize things with pickle. """
import pickle

julien = [
    'https://media.wmagazine.com/photos/59f1031ad473f932b6e964c5/4:3/w_1536/JULIEN_WMAG_37342.jpg',
    'https://f4.bcbits.com/img/a4215132093_10.jpg',
    'https://static01.nyt.com/images/2017/10/23/arts/23BAKER1/23BAKER1-superJumbo.jpg',
    'http://thebaybridged.com/wp-content/uploads/2017/02/Julien-Baker-at-GAMH-for-Noise-Pop-25-by-Ian-Young-03.jpg',
    'https://www.out.com/sites/out.com/files/2016/03/23/julien-baker-750.jpg',
    'http://static1.1.sqspcdn.com/static/f/828259/27325798/1478651908163/julienbaker1464753676527.png?token=VcH82OrcSIGKNKA1NYO%2FmIiHz2Y%3D',
    'http://diymag.com/media/img/Artists/J/Julien-Baker/Primavera-2016/_1500xAUTO_crop_center-center_75/Julien-Baker-Primavera-2016-20160602-Emma-Swann-7535.jpg',
    'https://static.stereogum.com/uploads/2017/10/julien_jleiby_001-1-1508858086-1498x1000.jpg',
    'http://pixel.nymag.com/imgs/daily/vulture/2015/10/19/19-julien-baker.w750.h560.2x.jpg',
    'http://thefader-res.cloudinary.com/private_images/w_760,c_limit,f_auto,q_auto:eco/170816_JulienBaker_3821_WEB_zmieth/julien-baker-turn-out-the-lights-sprained-ankle-interview.jpg',
    'http://img2-ak.lst.fm/i/u/arO/9874c6ba6183ca27e9fcd56a6586c812',
    'http://diymag.com/media/img/Artists/J/Julien-Baker/05-06-17-Bush-Hall/_1500xAUTO_crop_center-center_75/20170605213357-Julien-Baker-Ph-CFaruolo.jpg',
    'https://video-images.vice.com/articles/57a20706078424ded0752f90/lede/1484861775120-JulienBaker_2.jpeg'
]

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



with open('src/images/julien.pickle', 'wb') as f:
    pickle.dump(julien, f, pickle.HIGHEST_PROTOCOL)

with open('src/texts/commands.pickle', 'wb') as f:
    pickle.dump(commands, f, pickle.HIGHEST_PROTOCOL)