
def file_to_bytes(path):
    """
    Recibe el path de un archivo
    y retorna los bytes que contiene
    """
    # rb = read binary
    with open(path, 'rb') as file:
        return file.read()


def to_int(databytes):
    """
    Recibe un objeto 'bytes' y entrega
    el número que representa según little endian.
    Equivalente a:
        int.from_bytes(databytes, byteorder='little')
    """
    size = len(databytes)
    return sum(databytes[i] << (i * 8) for i in range(size))


class WAVMdata:
    """
    Clase con métodos estáticos útiles
    para trabajar con metadata de un .wav
    """
    @staticmethod
    def get_metadata(header):
        """
        Recibe el header de un archivo .wav (primeros 44 bytes)
        Y retorna un diccionario con su metadata
        """

        # Extraer informacion
        mdata = dict()
        mdata["riff"] = header[:4]
        mdata["size"] = to_int(header[4:8]) + 8
        mdata["wave"] = header[8:12]
        mdata["fmt"] = header[12:16]
        mdata["16"] = to_int(header[16:20])
        mdata["type"] = to_int(header[20:22])
        mdata["nch"] = to_int(header[22:24])
        mdata["fs"] = to_int(header[24:28])
        mdata["bps"] = to_int(header[34:36])
        mdata["init"] = header[36:40]
        mdata["datalen"] = to_int(header[40:44])

        print(mdata)

        # Comprueba que los bytes 28:32, 32:34 tengan el formato correcto
        # Y que la diferencia entre datalen y size sea 44 (tamaño del header)
        if to_int(header[28:32]) != mdata["fs"] * mdata["bps"] * mdata["nch"] / 8\
                or to_int(header[32:34]) != mdata["bps"] * mdata["nch"] / 8\
                or mdata["datalen"] != mdata["size"] - 44:
            print("Houston, tenemos un problema")

        return mdata

    @staticmethod
    def write_mdata(mdata, file):
        """
        Recibe una metadata (diccionario) y un archivo de output,
        y escribe en el archivo un header de .wav con la metadata especificada
        """
        # Nota: num.to_bytes(n, byteorder='little')
        #   num: número entero
        #   n: número de bytes que se desean
        #   retorna: un objeto de n bytes, que representa a num en little endian
        file.write(mdata["riff"])
        file.write((mdata["size"] - 8).to_bytes(4, byteorder='little'))
        file.write(mdata["wave"])
        file.write(mdata["fmt"])
        file.write(mdata["16"].to_bytes(4, byteorder='little'))
        file.write(mdata["type"].to_bytes(2, byteorder='little'))
        file.write(mdata["nch"].to_bytes(2, byteorder='little'))
        file.write(mdata["fs"].to_bytes(4, byteorder='little'))
        file.write(int(mdata["fs"] * mdata["bps"] * mdata["nch"] / 8).to_bytes(
            4, byteorder='little'
        ))
        file.write(int(mdata["bps"] * mdata["nch"] / 8).to_bytes(
            2, byteorder='little'
        ))
        file.write(mdata["bps"].to_bytes(2, byteorder='little'))
        file.write(mdata["init"])
        file.write((mdata["datalen"]).to_bytes(4, byteorder='little'))


class Filter:
    def __init__(self, data, k, n):
        """
        Las instancias de esta clase filtran las altas frecuencias de un audio
            data: objeto clase bytes con las muestras de audio
            k: Frecuencia de muestreo dividida en la frecuencia de corte
            n: orden del filtro
        """
        self.data = data
        self.k = k
        self.n = n

    def low_pass_filter(self, data):
        """
        Aplica un filtro pasabajos de primer orden a los datos
        y retorna la señal filtrada (lista de ints)
        """
        new_data = list()
        out_prev = data[0]

        for i in range(len(data)):
            new_data.append(int((data[i] + self.k*out_prev) / (self.k+1)))
            out_prev = new_data[-1]

        return new_data

    def split_channels(self):
        """
        Separa ambos canales de audio
        Retorna un diccionario de muestras para cada canal
        """
        b = {0: bytearray(), 1: bytearray()}
        out = {0: list(), 1: list()}
        # Separa las muestras de cada canal
        for i in range(0, len(data), 2):
            b[int(i/2) % 2].extend(data[i:i+2])

        for ch in range(2):
            for i in range(0, len(b[ch]), 2):
                # Decodifica los 2 bytes que corresponden a la muestra
                #   recordar que este audio tiene 16 bits por muestra (bps)
                number = to_int(b[ch][i:i+2])
                sample = (number-(2**16-1)) if number >= 2**15 else number
                out[ch].append(sample)

        return out

    @staticmethod
    def sample_to_bytes(sample):
        """
        Recibe una muestra (número de 0 a 2**16-1)
        y entrega dos bytes que la representan
        en little endian, con código complemento de 2 para representar signo
        """
        if (sample < 0):
            sample = 2**16-1 + sample
        return sample.to_bytes(2, byteorder='little')

    @staticmethod
    def plot(*args):
        """
        Recibe señales que se desee graficar
        Y muestra todas ellas en un mismo gráfico
        """
        import numpy as np
        from pylab import plt
        plotargs = []

        for arg in args:
            x = np.arange(0, len(arg))
            y = np.array([int(i) for i in arg])
            plotargs.extend([x, y])

        plt.plot(*plotargs)
        plt.show()

    def filter(self):
        """
        Retorna los datos filtrados,
        y listos para escribirse en un .wav
        """
        channels = Filter.split_channels(self.data)
        filtered = {0: self.low_pass_filter(channels[0]),
                    1: self.low_pass_filter(channels[1])}

        # Se aplica el filtro varias veces, para cada canal
        for _ in range(self.n-1):
            filtered[0] = self.low_pass_filter(filtered[0])
            filtered[1] = self.low_pass_filter(filtered[1])

        Filter.plot(channels[0], filtered[0])
        data = bytearray()
        for i in range(len(filtered[0])):
            data.extend(Filter.sample_to_bytes(filtered[0][i]))
            data.extend(Filter.sample_to_bytes(filtered[1][i]))

        return data


if __name__ == "__main__":
    filename = "chirp"
    data = file_to_bytes("{}.wav".format(filename))
    header = data[:44]
    data = data[44:]
    mdata = WAVMdata.get_metadata(header)

    k = 1               # Fs / Fcorte del filtro
    n = 10              # Orden del filtro
    f = 1               # Ajuste de frecuencia
    lpfilter = True     # Filtrar?

    # Filtramos la data
    if lpfilter:
        filtro = Filter(data, k, n)
        data = filtro.filter()

    # Modificamos frecuencia de muestreo en la metadata 3:)
    mdata["fs"] = int(mdata["fs"] * f)

    if lpfilter:
        filename += "_k{}_n{}".format(k, n)
    filename += "_f{}".format(f)

    # wb: write bynary
    with open("{}.wav".format(filename), "wb") as file:
        WAVMdata.write_mdata(mdata, file)
        file.write(data)