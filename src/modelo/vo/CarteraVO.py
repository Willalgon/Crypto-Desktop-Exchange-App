class CarteraVO:
    def __init__(self, saldo_fiat, valor_activos, patrimonio_total):
        self.__saldo_fiat = saldo_fiat
        self.__valor_activos = valor_activos
        self.__patrimonio_total = patrimonio_total

    @property
    def saldo_fiat(self): return self.__saldo_fiat
    @property
    def valor_activos(self): return self.__valor_activos
    @property
    def patrimonio_total(self): return self.__patrimonio_total

