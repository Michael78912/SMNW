class TerrainTemplate:
    @classmethod
    def load_text(cls):
        terrain_texts = {}
        terrain2dlist_texts = {}
        for text in os.listdir('terrains'):
            a = text.split('.')[0]
            terrain_texts[a] = open('terrains\\' + text).read()

        for terrain, key in zip(terrain_texts.values(), terrain_texts.keys()):
            if terrain.startswith('@'):
                # remove @ symbol
                header = terrain.split('\n')[0][1:]
                terrain = '\n'.join(terrain.split('\n')[1:])

                header = header.split('|')

                # remove all whitespace

                header = [part.strip().replace(' ', '').replace('\0', '')
                          .replace('\t', '').replace('\n', '').replace('\r', '') for part in header]

                for command in header:
                    parts = command.split('=')
                    if not parts[0] in ('air', 'water', 'size'):
                        raise SyntaxError(
                            '%a is not a valid command for header' % parts[1])
                    else:
                        item = eval(parts[1])
                        exec('cls.{} = {}'.format(*parts))

            lines = []
            for line in terrain.split('\n'):
                if ';' in line:
                    line = line.split(';')[0].strip()
                # dont append blank lines!
                if line != '':
                    lines.append(line)

            terrain2dlist = []
            for line in lines:
                chars = []
                for char in line:
                    chars.append(char)
                terrain2dlist.append(chars)

            terrain2dlist_texts[key] = terrain2dlist

        cls.terrain2dlist_texts = (terrain2dlist_texts) if isinstance(
            terrain2dlist_texts, list) else terrain2dlist_texts
