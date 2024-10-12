class filme:
    def __init__(self, nome='', autor='', desc=''):
        self.__nome = nome
        self.__autor = autor
        self.__desc = desc

    def setNome(self, nome): 
        self.__nome = nome

    def getNome(self): 
        return self.__nome
    
    def setAutor(self, autor): 
        self.__autor = autor

    def getAutor(self): 
        return self.__autor
    
    def setDesc(self, desc): 
        self.__desc = desc

    def getDesc(self): 
        return self.__desc