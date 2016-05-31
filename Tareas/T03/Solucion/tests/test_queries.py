query1 = 'EMPRESTA pokemon_nombre DE pokemon ONDE (pokemon_id_especie <= 151);'
query1_res = ['bulbasaur', 'ivysaur', 'venusaur', 'charmander', 'charmeleon',
              'charizard', 'squirtle', 'wartortle', 'blastoise', 'caterpie',
              'metapod', 'butterfree', 'weedle', 'kakuna', 'beedrill']

query2 = 'EMPRESTA PROMEDIO(pokemon_peso) DE pokemon;'
query2_res = [636.0961775585697]
query3 = 'EMPRESTA MIN(pokemon_experiencia_base) DE pokemon;'
query3_res = [36]
query4 = 'EMPRESTA MATS(pokemon_altura) DE pokemon;'
query4_res = [145]
query5 = "EMPRESTA pokemon_nombre DE pokemon " \
         "ONDE (pokemon_nombre PARECIO A 'mega');"
query5_res = ['meganium', 'yanmega', 'venusaur-mega', 'charizard-mega-x',
              'charizard-mega-y', 'blastoise-mega', 'alakazam-mega',
              'gengar-mega', 'kangaskhan-mega', 'pinsir-mega',
              'gyarados-mega', 'aerodactyl-mega', 'mewtwo-mega-x',
              'mewtwo-mega-y', 'ampharos-mega']
query6 = 'EMPRESTA DIVERGENTE pokemon_nombre DE pokemon, encuentros ' \
         'ONDE ((encuentro_pokemon_id = pokemon_id) ' \
         'Y (encuentro_min ENTRE (30 Y 60))) ' \
         'ORDENATELOS X pokemon_peso PA BAJO SOLO 10;'
query6_res = ['metagross', 'steelix', 'wailord', 'golurk', 'hippowdon',
              'mamoswine', 'beartic', 'hariyama', 'gyarados', 'lapras']
query7 = '(EMPRESTA pokemon_id DE pokemon ONDE (pokemon_altura > 10)) ' \
         'COMUN CN (EMPRESTA pokemon_id DE pokemon ONDE (pokemon_peso < 200));'
query7_res = [5, 23, 38, 45, 49, 71, 92, 93, 110, 147, 148, 153, 178, 206, 327,
              329, 354, 426, 549, 561, 666, 671, 10031, 10056, 10080, 10081,
              10082, 10083, 10084, 10085]
query8 = '(EMPRESTA pokemon_id DE pokemon ONDE (pokemon_experiencia_base ' \
         'ENTRE (100 Y 150))) SACALE (EMPRESTA pokemon_id DE pokemon ' \
         'ONDE (pokemon_id EN (EMPRESTA DIVERGENTE pokemon_id DE pokemon ' \
         'ONDE (pokemon_id != 2))));'
query8_res = [2]
query9 = "EMPRESTA pokemon_id DE pokemon ONDE " \
         "((EXISTE (EMPRESTA estadistica_nombre DE estadisticas)) " \
         "Y (pokemon_nombre PARECIO A 'pikachu'));"
query9_res = [25, 10080, 10081, 10082, 10083, 10084, 10085]
query10 = 'EMPRESTA pokemon_nombre DE pokemon, poke_estadisticas ' \
          'ONDE (pokemon_id = poke_estadisticas_pokemon_id) ' \
          'AGRUPATELOS X pokemon_nombre ' \
          'TENIENDO (PROMEDIO(poke_estadisticas_base) >= 100);'
query10_res = ['aerodactyl-mega', 'aggron-mega', 'ampharos-mega', 'arceus',
               'blastoise-mega', 'blaziken-mega', 'celebi', 'charizard-mega-x',
               'charizard-mega-y', 'cresselia', 'darkrai', 'deoxys-attack',
               'deoxys-defense', 'deoxys-normal', 'deoxys-speed', 'dialga',
               'diancie', 'diancie-mega', 'dragonite', 'gallade-mega',
               'garchomp', 'garchomp-mega', 'gardevoir-mega', 'genesect',
               'gengar-mega', 'giratina-altered', 'giratina-origin',
               'goodra', 'groudon', 'groudon-primal', 'gyarados-mega',
               'heatran', 'heracross-mega', 'ho-oh', 'hoopa', 'hoopa-unbound',
               'houndoom-mega', 'hydreigon', 'jirachi', 'kyogre',
               'kyogre-primal', 'kyurem', 'kyurem-black', 'kyurem-white',
               'landorus-incarnate', 'landorus-therian', 'latias',
               'latias-mega', 'latios', 'latios-mega', 'lucario-mega', 'lugia',
               'manaphy', 'meloetta-aria', 'meloetta-pirouette', 'metagross',
               'metagross-mega', 'mew', 'mewtwo', 'mewtwo-mega-x',
               'mewtwo-mega-y', 'palkia', 'pinsir-mega', 'rayquaza',
               'rayquaza-mega', 'regigigas', 'reshiram', 'salamence',
               'salamence-mega', 'sceptile-mega', 'scizor-mega', 'shaymin-land',
               'shaymin-sky', 'slaking', 'steelix-mega', 'swampert-mega',
               'tyranitar', 'tyranitar-mega', 'venusaur-mega', 'victini',
               'volcanion', 'xerneas', 'yveltal', 'zekrom', 'zygarde']
