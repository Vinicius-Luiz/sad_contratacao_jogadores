from tkinter import *
from tkinter import messagebox
import Controller as Ctrl
import Params as prm

def send_values():
    liga.showSelected()
    posicoes.to_bool()
    json = dict()
    json['metodo_pesquisa'] = dict()
    json['metodo_pesquisa']['metodo'] = met_pesq.metodo.get()
    json['metodo_pesquisa']['valor']  = met_pesq.valor.get()
    json['posicao'] = posicoes.posicao.get()
    json['idade']   = idade_nac_reputacao.inputs['IDADE'].get()
    json['nacionalidade']           = idade_nac_reputacao.inputs['NACIONALIDADE'].get()
    json['reputacao_internacional'] = idade_nac_reputacao.inputs['REPUTACAO'].get()
    json['ligas'] = liga.ligas
    json['combo'] = combo_start.valor.get()
    Ctrl.Dataframe(json)
    messagebox.showinfo("Relatório", "O relatório foi concluído com sucesso!")

############################################################################
class Root():
    def __init__(self, title = ''):
        self.root = Tk()
        self.root.title(title)
        self.root['background'] = prm.COLOR_BG

        self.SCREEN_W = self.root.winfo_screenwidth()
        self.SCREEN_H = self.root.winfo_screenheight()

        self.set_geometry()
        self.set_min_max_size()
    
    def set_geometry(self):
        eixo_x = self.SCREEN_W/2 - prm.W/2
        eixo_y = self.SCREEN_H/2 - prm.H/2

        self.root.geometry('%dx%d+%d+%d' % (prm.W, prm.H, int(eixo_x), int(eixo_y)))

    def set_min_max_size(self):
        self.root.minsize(width = prm.W, height = prm.H)
        self.root.maxsize(width = prm.W, height = prm.H)

    def mainloop(self):
        self.root.mainloop()
############################################################################

class Title():
    def __init__(self, root, text):
        self.text = text
        self.frame = Frame(root, height = prm.H*0.05)

        self.lbl()
    
    def lbl(self):
        Label(self.frame, bg = prm.COLOR_FONT, fg = prm.COLOR_BG,
        text = self.text, font = ('calibri',16,'bold')).pack(fill=BOTH)
    
    def pack(self):
        self.frame.pack(fill=X)

class Metodo_Pesquisa():
    def __init__(self, root):
        self.height     = prm.H*0.15
        self.metodo     =  IntVar()
        self.valor      =  IntVar()
        self.text_valor = StringVar()
        self.text_input = {1: 'de compra', 2: 'do salário', 3: 'da cláusula'}
        self.set_metodo(1)
        
        self.frame = Frame(root, height = self.height,
        bg = prm.COLOR_BG)

        self.titlebox    = self.title('MÉTODO DE PESQUISA*')
        self.chkboxs     = self.lbl_chkbox()
        self.chkbox1     = self.chkbox('Compra', 1)
        self.chkbox2     = self.chkbox('Salário', 2)
        self.chkbox3     = self.chkbox('Cláusula', 3)
        self.inputboxs   = self.lbl_inputbox()
        self.inputbox    = self.inputvalue()
        self.inputextbox = self.inputtext()

        self.chkbox1.select()
        self.chkbox2.deselect()
        self.chkbox3.deselect()

    def set_metodo(self, value):
        self.metodo.set(value)
        self.text_valor.set(f'Valor {self.text_input[self.metodo.get()]} (€)')   
        try:
            self.inputextbox.config(text=self.text_valor.get())
        except:
            pass
    
    def title(self, text):
        return Label(self.frame, font = prm.FONT, text = text, 
        anchor = W,
        fg = prm.COLOR_FONT, bg = prm.COLOR_BG)

    def lbl_chkbox(self):
        return Label(self.frame, 
        bg = prm.COLOR_BG)
    
    def lbl_inputbox(self):
        return Label(self.frame, 
        bg = prm.COLOR_BG)

    def chkbox(self, text, value):
        return Radiobutton(self.chkboxs, text = text, font = prm.FONT_OP,
        bg = prm.COLOR_BG, activebackground = prm.COLOR_BG, fg= prm.COLOR_FONT,
        width = prm.converter_pixel_chr(prm.W*0.33), anchor = W,
        value = value, variable = self.metodo, command = lambda: self.set_metodo(value))

    def inputvalue(self):
        return Entry(self.inputboxs, font = prm.FONT_OP,
        fg = prm.COLOR_FONT_INPUT, bg = prm.COLOR_INPUT,
        width = prm.converter_pixel_chr(prm.W*0.3),
        textvariable= self.valor) 
    
    def inputtext(self):
        return Label(self.inputboxs, font = prm.FONT,
        anchor = W, text = self.text_valor.get(),
        width = prm.converter_pixel_chr(prm.W*0.7),
        fg = prm.COLOR_FONT, bg = prm.COLOR_BG)
        
    def pack(self):
        self.titlebox.pack(fill=X)
        self.chkboxs.pack(fill=X)
        self.chkbox1.pack(side = LEFT)
        self.chkbox2.pack(side = LEFT)
        self.chkbox3.pack(side = LEFT)
        self.inputboxs.pack(fill=X)
        self.inputbox.pack(side = LEFT)
        self.inputextbox.pack(side = LEFT, padx = 2)

        self.frame.pack(fill=X, pady= prm.PADY, padx = prm.PADX)

class Posicao():
    def __init__ (self, root):
        self.height = prm.H*0.30
        self.posicao = StringVar()
        self.posicao.set('GK')

        self.frame = Frame(root, height = self.height)

        self.titlebox    = self.title('POSIÇÃO*')
        self.posboxs1    = self.lbl_pos()
        self.posboxs2    = self.lbl_pos()
        self.posboxs3    = self.lbl_pos()
        self.posbox1     = self.chkbutton(self.posboxs1, 'Goleiro', 'GK')
        self.posbox2     = self.chkbutton(self.posboxs1, 'Zagueiro', 'CB')
        self.posbox3     = self.chkbutton(self.posboxs1, 'Lateral-direito', 'RB')
        self.posbox4     = self.chkbutton(self.posboxs1, 'Lateral-Esquerdo ', 'LB')
        self.posbox5     = self.chkbutton(self.posboxs2, 'Volante', 'CDM')
        self.posbox6     = self.chkbutton(self.posboxs2, 'Meio-campo', 'CM')
        self.posbox7     = self.chkbutton(self.posboxs2, 'Meio-direito', 'RM')
        self.posbox8     = self.chkbutton(self.posboxs2, 'Meio-esquerdo', 'LM')
        self.posbox9     = self.chkbutton(self.posboxs2, 'Meio-ofensivo', 'CAM')
        self.posbox10    = self.chkbutton(self.posboxs3, 'Ponta-direito', 'RW')
        self.posbox11    = self.chkbutton(self.posboxs3, 'Ponta-esquerdo', 'LW')
        self.posbox12    = self.chkbutton(self.posboxs3, 'Segundo-atacante', 'CF')
        self.posbox13    = self.chkbutton(self.posboxs3, 'Centroavante', 'ST')
    
    def title(self, text):
        return Label(self.frame, font = prm.FONT, text = text, 
        anchor = W,
        fg = prm.COLOR_FONT, bg = prm.COLOR_BG)
    
    def lbl_pos(self):
        return Label(self.frame, bg = prm.COLOR_BG)
    
    def chkbutton(self, root, pos, cod):
        return Radiobutton(root, text = pos, font = prm.FONT_OP,
        bg = prm.COLOR_BG, fg= prm.COLOR_FONT, activebackground = prm.COLOR_BG,
        anchor = W, value = cod, variable = self.posicao)

    def to_bool(self):
        try:
            for k, v in self.posicoes.items():
                self.posicoes[k] = v.get()
        except:
            pass
    
    def pack(self):
        self.titlebox.pack(fill=X)
        self.posbox1.pack(fill= X)
        self.posbox2.pack(fill= X)
        self.posbox3.pack(fill= X)
        self.posbox4.pack(fill= X)
        self.posbox5.pack(fill= X)
        self.posbox6.pack(fill= X)
        self.posbox7.pack(fill= X)
        self.posbox8.pack(fill= X)
        self.posbox9.pack(fill= X)
        self.posbox10.pack(fill= X)
        self.posbox11.pack(fill= X)
        self.posbox12.pack(fill= X)
        self.posbox13.pack(fill= X)
        self.posboxs1.pack(side = LEFT, fill=BOTH, expand = True) 
        self.posboxs2.pack(side = LEFT, fill=BOTH, expand = True) 
        self.posboxs3.pack(side = LEFT, fill=BOTH, expand = True) 
        self.frame.pack(fill=X, pady= prm.PADY, padx = prm.PADX)

class Idade_Nacion_Reputacao():
    def __init__(self, root):
        self.height = prm.H*0.10
        self.inputs = {'IDADE': StringVar(), 'NACIONALIDADE': StringVar(), 'REPUTACAO': StringVar()}
        self.inputs['IDADE'].set('Todos')
        self.inputs['NACIONALIDADE'].set('Todos')
        self.inputs['REPUTACAO'].set('Todos')

        self.paises = ['Argentina','Poland','Portugal','Brazil','Belgium','Slovenia','France','Germany','England','Korea Republic','Netherlands',
                        'Senegal','Egypt','Italy','Spain','Uruguay','Costa Rica','Norway','Croatia','Scotland','Algeria','Slovakia','Denmark','Switzerland','Hungary','Gabon',
                        'Serbia','Nigeria','Morocco','Sweden','Austria','Montenegro',"Côte d'Ivoire",'Mexico','Bosnia and Herzegovina','Finland','Greece','Armenia','Colombia','Cameroon','Ghana','Wales','Russia','Turkey','United States','Jamaica','Canada','Czech Republic','Chile','Ukraine',
                        'Venezuela','Togo','Burkina Faso','Northern Ireland','Congo DR','Israel','Albania','Guinea','Iceland','China PR','New Zealand','Central African Republic','Peru','Mali','Japan','North Macedonia','Ecuador','Iran','Republic of Ireland','Angola','Romania','Mozambique',
                        'Cape Verde Islands','Australia','Paraguay','Tunisia','Kosovo','Zimbabwe','Zambia','Libya','Suriname','Saudi Arabia','Syria','Gambia','Kenya','Georgia','Equatorial Guinea','Panama','Dominican Republic','Trinidad and Tobago','Honduras','Guinea Bissau','Liberia','Curacao','Tanzania','Benin','Cyprus','South Africa','Uzbekistan','Congo','Madagascar','Moldova','Cuba','Saint Kitts and Nevis','Philippines','Fiji','United Arab Emirates','Luxembourg','Namibia','Chad','Lithuania','Bolivia','Comoros','Thailand','Bermuda',
                        'Burundi','Antigua and Barbuda','Malawi','Haiti','Bulgaria','Sierra Leone','Kazakhstan','Montserrat','Chinese Taipei','El Salvador','Niger','Malta','Uganda','Belarus','Jordan','India','Iraq','Puerto Rico','Azerbaijan','Mauritania',
                        'Eritrea','Mauritius','Lebanon','Sudan','Grenada','Latvia','Guam','Kyrgyzstan','Guyana','Faroe Islands','Papua New Guinea','Ethiopia','Andorra','Korea DPR','Saint Lucia','Afghanistan','Vietnam','Belize','Guatemala','Palestine','Bhutan','Barbados','Gibraltar','Malaysia','Estonia','South Sudan','Hong Kong','Indonesia']
        self.paises.sort()

        self.reputacao = ['Muito alta', 'Alta', 'Média', 'Baixa','Muito baixa']

        self.frame = Frame(root, height = self.height, bg = prm.COLOR_BG)

        self.idadebox         = self.lbl_idade()
        self.nacionalidadebox = self.lbl_nacionalidade()
        self.reputacaobox     = self.lbl_reputacao()
        
        self.titleboxI    = self.title('IDADE', 80)
        self.titleboxN    = self.title('NACIONALIDADE', 180)
        self.titleboxR    = self.title('REPUTAÇÃO INTERNACIONAL', 260)

        self.opt_menuI    = self.opt_menu('IDADE',  ['Todos', '<= 21', '22 - 27', '28 - 33', '34 - 39', '>= 40'])
        self.opt_menuN    = self.opt_menu('NACIONALIDADE', ['Todos']+self.paises)
        self.opt_menuR    = self.opt_menu('REPUTACAO',  ['Todos']+self.reputacao)

    def lbl_idade(self):
        return Label(self.frame, bg = prm.COLOR_BG)
            
    def lbl_nacionalidade(self):
        return Label(self.frame, bg = prm.COLOR_BG)

    def lbl_reputacao(self):
        return Label(self.frame, bg = prm.COLOR_BG)

    def title(self, text, width):
        if text == 'IDADE':
            return Label(self.idadebox, font = prm.FONT, text = text, 
            width=prm.converter_pixel_chr(width, pad = False),
            fg = prm.COLOR_FONT, bg = prm.COLOR_BG)
        if text == 'NACIONALIDADE':
            return Label(self.nacionalidadebox, font = prm.FONT, text = text, 
            width=prm.converter_pixel_chr(width, pad = False),
            fg = prm.COLOR_FONT, bg = prm.COLOR_BG)
        if text == 'REPUTAÇÃO INTERNACIONAL':
            return Label(self.reputacaobox, font = prm.FONT, text = text, 
            width=prm.converter_pixel_chr(width, pad = False),
            fg = prm.COLOR_FONT, bg = prm.COLOR_BG)

    def opt_menu(self, tipo, ranges):
        if tipo == 'IDADE':
            return OptionMenu(self.idadebox, self.inputs[tipo], *ranges)
        elif tipo == 'NACIONALIDADE':
            return OptionMenu(self.nacionalidadebox, self.inputs[tipo], *ranges)
        elif tipo == 'REPUTACAO':
            return OptionMenu(self.reputacaobox, self.inputs[tipo], *ranges)
    

    def pack(self):
        self.titleboxI.pack()
        self.titleboxN.pack()
        self.titleboxR.pack()

        self.opt_menuI.pack(fill=BOTH)
        self.opt_menuN.pack(fill=BOTH)
        self.opt_menuR.pack(fill=BOTH)

        self.idadebox.pack(side=LEFT)
        self.nacionalidadebox.pack(side=LEFT)
        self.reputacaobox.pack(side=LEFT)
        
        self.frame.pack(fill=X, pady= prm.PADY, padx = prm.PADX)

class Liga():
    def __init__(self, root):
        self.height = 0.3
        self.ligas  = []
        self.ligaslist = ['Todos','English Premier League','Italian Serie A','Spain Primera Division','French Ligue 1','German 1. Bundesliga','Holland Eredivisie','Portuguese Liga ZON SAGRES','Campeonato Brasileiro Série A','Paraguayan Primera División','Argentina Primera División','Ecuadorian Serie A','Scottish Premiership','Greek Super League',
                        'Austrian Football Bundesliga','Belgian Jupiler Pro League','Mexican Liga MX','Russian Premier League','Colombian Liga Postobón','Croatian Prva HNL','English League Championship','English League One','English League Two','English National League','Italian Serie B','Spanish Segunda División','German 2. Bundesliga',
                        'German 3. Bundesliga','French Ligue 2','Australian Hyundai A-League','Chilian Campeonato Nacional','Chinese Super League','Cypriot First Division','Czech Republic Gambrinus Liga','Danish Superliga','Finnish Veikkausliiga','Hungarian Nemzeti Bajnokság I','Indian Super League','Japanese J. League Division 1','Korean K League 1',
                        'Liga de Fútbol Profesional Boliviano','Norwegian Eliteserien','Peruvian Primera División','Polish T-Mobile Ekstraklasa','Rep. Ireland Airtricity League','Romanian Liga I', 'Saudi Abdul L. Jameel League','South African Premier Division','Swedish Allsvenskan','Swiss Super League','Turkish Süper Lig','UAE Arabian Gulf League',
                        'USA Major League Soccer','Ukrainian Premier League','Uruguayan Primera División','Venezuelan Primera División']
        
        self.frame = Frame(root, height = self.height, bg = prm.COLOR_BG)

        self.ligatitlebox    = self.title('LIGA')
        self.ligalistbox     = self.listbox()

        self.scrollbar = Scrollbar(root)
    
    def listbox(self):
        return Listbox(self.frame, selectmode=MULTIPLE,
        selectbackground=prm.COLOR_INPUT, height=5)

    def title(self, text):
        return Label(self.frame, font = prm.FONT, text = text,
        fg = prm.COLOR_FONT, bg = prm.COLOR_BG)

    def showSelected(self):
        self.ligas.clear()
        cname = self.ligalistbox.curselection()
        for i in cname:
            op = self.ligalistbox.get(i)
            self.ligas.append(op)

    def pack(self):
        self.ligatitlebox.pack(fill = X, expand = True)
        self.ligalistbox.pack(fill = X, expand = True)
        for i, league in enumerate(self.ligaslist):
            self.ligalistbox.insert(i, league)

        self.ligalistbox.activate(0)
        #Button(self.frame, text="Show Selected", command=self.showSelected).pack()
        
        self.scrollbar.pack(side = RIGHT, fill = Y) 
        self.ligalistbox.config(yscrollcommand = self.scrollbar.set) 
        self.scrollbar.config(command = self.ligalistbox.yview) 

        self.frame.pack(fill=X, pady= prm.PADY, padx = prm.PADX)

class Combinacoes():
    def __init__(self, root):
        self.height = 0.2
        self.valor      =  IntVar()
        self.valor.set(1)

        self.frame       = Frame(root, height = self.height, bg = prm.COLOR_BG)
        self.combos      = self.lbl_combo()
        self.titlebox    = self.title('QTDE DE COMBINAÇÕES')
        self.inputbox    = self.inputvalue()

        self.submit      = self.button()

    def lbl_combo(self):
        return Label(self.frame, bg = prm.COLOR_BG)

    def title(self, text):
        return Label(self.combos, font = prm.FONT, text = text,
        fg = prm.COLOR_FONT, bg = prm.COLOR_BG)

    def inputvalue(self):
        return Entry(self.combos, font = prm.FONT_OP,
        fg = prm.COLOR_FONT_INPUT, bg = prm.COLOR_INPUT, justify=CENTER,
        width = prm.converter_pixel_chr(prm.W*0.05),
        textvariable= self.valor) 
    
    def button(self):
        return Button(self.frame, text="Pesquisar", command= lambda: send_values(),
                    width = prm.converter_pixel_chr(prm.W*0.10),
                    bg = prm.COLOR_INPUT, activeforeground = prm.COLOR_BG, fg = prm.COLOR_BG,
                    font = prm.FONT)
    
    def pack(self):
        self.titlebox.pack()
        self.inputbox.pack()

        self.combos.pack(side = LEFT, fill = X)
        self.submit.pack(side = LEFT, fill = X, padx = 120)
        self.frame.pack(fill=X, pady= prm.PADY, padx = prm.PADX)


root                = Root('Busca de Jogadores')
title               = Title(root.root, 'ADVANCED PLAYER SEARCH')
met_pesq            = Metodo_Pesquisa(root.root)
posicoes            = Posicao(root.root)
idade_nac_reputacao = Idade_Nacion_Reputacao(root.root)
liga                = Liga(root.root)
combo_start         = Combinacoes(root.root)

title.pack()
met_pesq.pack()
posicoes.pack()
idade_nac_reputacao.pack()
liga.pack()
combo_start.pack()
root.mainloop()
