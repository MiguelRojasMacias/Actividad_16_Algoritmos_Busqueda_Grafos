from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, QGraphicsScene
from PySide2.QtGui import QPen, QColor, QTransform
from PySide2.QtCore import Slot
from ui_mainwindow import Ui_MainWindow
from Particulas import Particulas
from particula import Particula
import pprint

def sort_by_id(Particula):
    return Particula.id


# la clase mainwindow hereda lo de QMainWindow
class MainWindow(QMainWindow): 

    particula = Particula() 
    particulas = Particulas() #administra particulas
    #al declarar el objeto de manera globar ya podemos crear particulas

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Inicio_pushButton.clicked.connect(self.agregar_Particula_Inicio)
        self.ui.Final_pushButton.clicked.connect(self.agregar_Particula_Final)
        self.ui.pushButton_2.clicked.connect(self.mostrar_Particula)
        
        self.ui.actionAbrir.triggered.connect(self.action_abrir_archivo)
        self.ui.actionGuardar.triggered.connect(self.action_guardar_archivo)

        self.ui.mostrar_tabla_pushButton.clicked.connect(self.mostrar_tabla)
        self.ui.buscar_pushButton.clicked.connect(self.buscar_titulo)

        self.ui.dibujar.clicked.connect(self.dibujar)
        self.ui.limpiar.clicked.connect(self.limpiar)

        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        self.ui.idOrdenar_pushButton.clicked.connect(self.Ordenarid)
        self.ui.distanciaOrdenar_pushButton.clicked.connect(self.Ordenardistancia)
        self.ui.velocidadOrdenar_pushButton.clicked.connect(self.Ordenarvelocidad)

        self.ui.grafos_pushButton.clicked.connect(self.grafo)

        self.ui.actionRecorrido_Amplitud.triggered.connect(self.action_recorrido_amplitud)
        self.ui.actionRecorrido_Profundidad.triggered.connect(self.action_recorrido_profundidad)


    @Slot()
    def action_recorrido_amplitud(self):
        
        # -- RECORRIDO AMPLITUD --
        cola = []
        amplitud = []
        grafo = dict()

        for p in self.particulas.contenedor:
            origen = (p.origenX, p.origenY)
            destino =(p.destinoX,p.destinoY)
            distancia = (p.distancia)

            arista_origen = (origen,distancia)
            arista_destino = (destino,distancia)
            if origen in grafo:
                grafo[origen].append(arista_destino)
            else:
                grafo[origen] = [arista_destino]
            if destino in grafo:
                grafo[destino].append(arista_origen)
            else:
                grafo[destino] = [arista_origen]
        x = self.ui.origenX_spinBox.value()
        y = self.ui.origenY_spinBox.value()
        cola.append((x,y))
        amplitud.append((x,y))
        while True:
            if cola:
                padre = cola[0]
                del cola[0]
                adyacentes = grafo[padre]
                for a in adyacentes:
                    band=False
                    for i in amplitud:
                        if i == a[0]:
                            band = 1 
                            break
                        else:
                            band = 0 
                    if band == 0:
                        amplitud.append(a[0])
                        cola.append(a[0])

            else:
                break

        # -- IMPRESION -- 
        print("-- AMPLITUD --")    
        print(amplitud)
        print("\n")
        self.ui.salida.clear()
        self.ui.salida.insertPlainText("-- Amplitud --\n")
        self.ui.salida.insertPlainText(str(amplitud))

        

    @Slot()
    def action_recorrido_profundidad(self):
        # -- RECORRIDO PROFUNDIDAD --
        pila=[]
        profundidad=[]
        grafo = dict()
        x = self.ui.origenX_spinBox.value()
        y = self.ui.origenY_spinBox.value()
        nodo = (x,y)
        pila.append(nodo)
        profundidad.append(nodo)

        for n in self.particulas.contenedor:
            origen = (n.origenX,n.origenY)
            destino =(n.destinoX,n.destinoY)

            if origen in grafo:
                grafo[origen].append(destino)
            else:
                grafo[origen] = [destino]
            if destino in grafo:
                grafo[destino].append(origen)
            else:
                grafo[destino] = [origen]

        while pila:
            nodo  = tuple(pila[-1])
            del pila[-1]

            for i in grafo.get(nodo):
                temp = tuple(i)
                if temp not in profundidad:
                    profundidad.append(temp)
                    pila.append(temp)
        # -- IMPRESION --
        print("-- PROFUNDIDAD --")
        print(profundidad)
        self.ui.salida.clear()
        self.ui.salida.insertPlainText("-- Profundidad --\n")
        self.ui.salida.insertPlainText(str(profundidad))
            


    @Slot()
    def grafo(self):
        grafo = dict()
        for p in self.particulas.contenedor:
            origen = (p.origenX, p.origenY)
            destino = (p.destinoX, p.destinoY)
            distancia = (p.distancia)

            arista_origen = (origen,distancia)
            arista_destino = (destino,distancia)

            if origen in grafo:
                grafo[origen].append(arista_destino)
            else:
                grafo[origen] = [arista_destino]
            if destino in grafo:
                grafo[destino].append(arista_origen)
            else:
                grafo[destino] = [arista_origen]
            
            impresion = pprint.pformat(grafo, width=40)
            impresion+= '\n'

        self.ui.salida.insertPlainText(impresion)


    @Slot()
    def Ordenarid(self):
        self.particulas.contenedor.sort(key=sort_by_id)
    
    @Slot()
    def Ordenardistancia(self):
        self.particulas.contenedor.sort(key=lambda Particula: Particula.distancia, reverse=True)
        
    @Slot()
    def Ordenarvelocidad(self):
        self.particulas.contenedor.sort(key=lambda Particula: Particula.velocidad)

    def wheelEvent(self, event):
        if event.delta() > 0:
            self.ui.graphicsView.scale(1.2, 1.2)
        else:
            self.ui.graphicsView.scale(0.8, 0.8)


    @Slot()
    def dibujar(self): 
        pen = QPen()
        pen.setWidth(2) 
        for particula in self.particulas:
            R = particula.colorR
            G = particula.colorG
            B = particula.colorB
            color = QColor (R,G,B)
            pen.setColor(color)
            self.scene.addEllipse(particula.origenX, particula.origenY,3,3,pen)
            self.scene.addEllipse(particula.destinoX, particula.destinoY,3,3,pen)
            self.scene.addLine(particula.origenX+3, particula.origenY+3, particula.destinoX, particula.destinoY, pen)
            print(color)


    @Slot()
    def limpiar(self):
        self.scene.clear()

    @Slot()
    def buscar_titulo(self):
        id = self.ui.buscar_lineEdit.text()
        encontrado = False
        for particula in self.particulas:
            if id == particula.id:
                self.ui.tabla.clear() #vacia la filas para poner el libro
                self.ui.tabla.setRowCount(1) #nada mas tendra una fila
                id_widget = QTableWidgetItem(particula.id)
                origenX_widget = QTableWidgetItem(str(particula.origenX))
                origenY_widget = QTableWidgetItem(str(particula.origenY))
                destinoX_widget = QTableWidgetItem(str(particula.destinoX))
                destinoY_widget = QTableWidgetItem(str(particula.destinoY))
                velocidad_widget = QTableWidgetItem(str(particula.velocidad))
                colorR_widget = QTableWidgetItem(str(particula.colorR))
                colorG_widget = QTableWidgetItem(str(particula.colorG))
                colorB_widget = QTableWidgetItem(str(particula.colorB))
                distancia_widget = QTableWidgetItem(str(particula.distancia))

                self.ui.tabla.setItem(0, 0,id_widget)
                self.ui.tabla.setItem(0, 1,origenX_widget)
                self.ui.tabla.setItem(0, 2,origenY_widget)
                self.ui.tabla.setItem(0, 3,destinoX_widget)
                self.ui.tabla.setItem(0, 4,destinoY_widget)
                self.ui.tabla.setItem(0, 5,velocidad_widget)
                self.ui.tabla.setItem(0, 6,colorR_widget)
                self.ui.tabla.setItem(0, 7,colorG_widget)
                self.ui.tabla.setItem(0, 8,colorB_widget)
                self.ui.tabla.setItem(0, 9,distancia_widget)
                encontrado = True
                return 
        if not encontrado:
            QMessageBox.warning(
                self,
                "Atencion",
                f'ERROR -> La Particula con el ID: "{id}" no se encontro'
            )
            



    @Slot()
    def mostrar_tabla(self):
        self.ui.tabla.setColumnCount(10)
        headers = ["ID","Origen X","Origen Y","Destino X", "Destino Y","Velocidad","Color R","Color G","Color B","Distancia"]
        self.ui.tabla.setHorizontalHeaderLabels(headers) # en la cabecera imprime los nombres

        self.ui.tabla.setRowCount(len(self.particulas)) # crea la cantidad de lineas dependiendo de las particulas que hemmos insertado

        row = 0
        for particula in self.particulas:
            id_widget = QTableWidgetItem(particula.id)
            origenX_widget = QTableWidgetItem(str(particula.origenX))
            origenY_widget = QTableWidgetItem(str(particula.origenY))
            destinoX_widget = QTableWidgetItem(str(particula.destinoX))
            destinoY_widget = QTableWidgetItem(str(particula.destinoY))
            velocidad_widget = QTableWidgetItem(str(particula.velocidad))
            colorR_widget = QTableWidgetItem(str(particula.colorR))
            colorG_widget = QTableWidgetItem(str(particula.colorG))
            colorB_widget = QTableWidgetItem(str(particula.colorB))
            distancia_widget = QTableWidgetItem(str(particula.distancia))

            self.ui.tabla.setItem(row, 0,id_widget)
            self.ui.tabla.setItem(row, 1,origenX_widget)
            self.ui.tabla.setItem(row, 2,origenY_widget)
            self.ui.tabla.setItem(row, 3,destinoX_widget)
            self.ui.tabla.setItem(row, 4,destinoY_widget)
            self.ui.tabla.setItem(row, 5,velocidad_widget)
            self.ui.tabla.setItem(row, 6,colorR_widget)
            self.ui.tabla.setItem(row, 7,colorG_widget)
            self.ui.tabla.setItem(row, 8,colorB_widget)
            self.ui.tabla.setItem(row, 9,distancia_widget)

            row += 1 # incrementamos el contador de fila para que no se escriban encima
        
    @Slot()
    def action_abrir_archivo(self):
        #print('Abrir_archivo')
        ubicacion = QFileDialog.getOpenFileName(
            self,
            'Abrir Archivo', #el nombre del archivo
            '.', #donde lo va a guardar, en este caso en la carpeta del proyecto
            'JSON (*.json)' #Tipo de formato
        )[0]
        if self.particulas.abrir(ubicacion):
            QMessageBox.information(
                self,
                "Éxito",
                "Se abrió el archivo " + ubicacion
            )
        else:
            QMessageBox.information(
                self,
                "Error",
                "Error al abrir el archivo " + ubicacion
            )
        
    @Slot()
    def action_guardar_archivo(self):
        #print('Guardar_archivo')
        ubicacion = QFileDialog.getSaveFileName(
            self,
            'Guardar Archivo', #el nombre del archivo
            '.', #donde lo va a guardar, en este caso en la carpeta del proyecto
            'JSON (*.json)' #Tipo de formato
        )[0]
        print(ubicacion)
        if self.particulas.guardar(ubicacion):
            QMessageBox.information(
                self, #desde donde se manda
                "Éxito", #nombre de la ventana
                "Se pudo crear el archivo " + ubicacion #mensaje
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo crear el archivo " + ubicacion
            )
            

    @Slot()
    def agregar_Particula_Inicio(self):
        id = self.ui.ID_lineEdit.text()
        origenX = self.ui.origenX_spinBox.value()
        origenY = self.ui.origenY_spinBox.value()
        destinoX = self.ui.destinoX_spinBox.value()
        destinoY = self.ui.destinoY_spinBox.value()
        velocidad = self.ui.velocidad_spinBox.value()
        colorR = self.ui.R_spinBox.value()
        colorG = self.ui.G_spinBox.value()
        colorB = self.ui.B_spinBox.value()

        particula = Particula(id, origenX, origenY, destinoX, destinoY, velocidad, colorR, colorG, colorB)
        self.particulas.agregar_inicio(particula)
            

    @Slot()
    def agregar_Particula_Final(self):
        id = self.ui.ID_lineEdit.text()
        origenX = self.ui.origenX_spinBox.value()
        origenY = self.ui.origenY_spinBox.value()
        destinoX = self.ui.destinoX_spinBox.value()
        destinoY = self.ui.destinoY_spinBox.value()
        velocidad = self.ui.velocidad_spinBox.value()
        colorR = self.ui.R_spinBox.value()
        colorG = self.ui.G_spinBox.value()
        colorB = self.ui.B_spinBox.value()

        particula = Particula(id, origenX, origenY, destinoX, destinoY, velocidad, colorR, colorG, colorB)
        self.particulas.agregar_final(particula)


    @Slot()
    def mostrar_Particula(self):
        #self.particulas.mostrar()
        self.ui.salida.clear(
            
        )
        self.ui.salida.insertPlainText(str(self.particulas))