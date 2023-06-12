class config_parser(object):
    def __init__(self):
        file=open('config.txt','r',encoding='utf-8')
        data=file.read().split('\n')
        self.config={'p': 60275702009245096385686171515219896416297121499402250955537857683885541941187, 'a': 54492052985589574080443685629857027481671841726313362585597978545915325572248, 'b': 45183185393608134601425506985501881231876135519103376096391853873370470098074, 'G': [29905514254078361236418469080477708234343499662916671209092838329800180225085, 2940593737975541915790390447892157254280677083040126061230851964063234001314], 'pb': [30466142855137288468788190552058120832437161821909553502398316083968243039754, 53312363470992020232197984648603141288071418796825192480967103513769615518274], 'k': 34550576952843389977837539438321907097625575044301827052096699664811526290255, 'w': 5, 'N': 500, 'floor': 2, 'ceil': 10}
        for i in data:
            if '#' in i or not i:
                continue
            line=i.split('=')
            if len(line[1].split())==2:
                self.config[line[0]]=list(map(int,line[1].split()))
            else:
                self.config[line[0]] = int(line[1])
        if self.config['floor']<2:
            raise Exception('floor must >=2')
        if self.config['ceil'] < self.config['floor']:
            raise Exception('ceil is less than floor')
if __name__ == '__main__':
    a=config_parser()
    print(a.config)