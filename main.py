"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas
Curso: Programación - Código: 213023
UNAD - Universidad Nacional Abierta y a Distancia
"""

from datetime import datetime
from modelos import *
from excepciones import *


class GestorLogs:
    """Clase para manejar el registro de eventos y errores"""
    ARCHIVO_LOGS = "logs.txt"
    
    @staticmethod
    def registrar(evento: str, nivel: str = "INFO"):
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        linea = f"[{timestamp}] [{nivel}] {evento}\n"
        with open(GestorLogs.ARCHIVO_LOGS, "a", encoding="utf-8") as f:
            f.write(linea)
    
    @staticmethod
    def info(mensaje: str):
        GestorLogs.registrar(mensaje, "INFO")
    
    @staticmethod
    def error(mensaje: str):
        GestorLogs.registrar(mensaje, "ERROR")
    
    @staticmethod
    def advertencia(mensaje: str):
        GestorLogs.registrar(mensaje, "ADVERTENCIA")


class SistemaReservas:
    """Clase principal que gestiona todo el sistema"""
    def _init_(self):
        self.clientes = {}
        self.servicios = []
        self.reservas = []
        self._inicializar_servicios()
        GestorLogs.info("✅ Sistema iniciado correctamente")
    
    def _inicializar_servicios(self):
        self.servicios.append(ReservaSalas())
        self.servicios.append(AlquilerEquipos())
        self.servicios.append(AsesoriaEspecializada())
    
    def registrar_cliente(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        try:
            if id_cliente in self.clientes:
                raise ClienteDuplicadoError(f"El cliente con ID {id_cliente} ya está registrado")
            cliente = Cliente(id_cliente, nombre, correo, telefono)
            self.clientes[id_cliente] = cliente
            GestorLogs.info(f"Cliente registrado: {nombre} (ID: {id_cliente})")
            return cliente
        except (DatoInvalidoError, ClienteDuplicadoError) as e:
            GestorLogs.error(f"Error al registrar cliente: {e}")
            raise
    
    def listar_servicios(self):
        for idx, servicio in enumerate(self.servicios, 1):
            print(f"{idx}. {servicio.describir()}")
    
    def crear_reserva(self, id_cliente: str, indice_servicio: int, duracion: float):
        try:
            if id_cliente not in self.clientes:
                raise DatoInvalidoError(f"Cliente con ID {id_cliente} no encontrado")
            if indice_servicio < 0 or indice_servicio >= len(self.servicios):
                raise DatoInvalidoError("Índice de servicio no válido")
            
            cliente = self.clientes[id_cliente]
            servicio = self.servicios[indice_servicio]
            reserva = Reserva(cliente, servicio, duracion)
            self.reservas.append(reserva)
            GestorLogs.info(f"Reserva creada: {servicio.nombre} — Cliente: {cliente.nombre}")
            return reserva
        except (ServicioNoDisponibleError, ReservaInvalidaError, DatoInvalidoError) as e:
            GestorLogs.error(f"Error al crear reserva: {e}")
            raise
    
    def listar_reservas(self):
        if not self.reservas:
            print("📋 No hay reservas registradas")
            return
        for i, reserva in enumerate(self.reservas, 1):
            print(f"\n--- Reserva {i} ---")
            print(reserva)
            print(f"   Costo total: ${reserva.calcular_total(impuesto=0.19):,.2f}")
    
    def ejecutar_pruebas(self):
        """Ejecuta al menos 10 operaciones completas como exige el enunciado"""
        print("=" * 60)
        print("   SISTEMA DE GESTIÓN DE RESERVAS — PRUEBAS DEL SISTEMA")
        print("=" * 60)
        
        sistema = SistemaReservas()
        
        print("\n📌 OPERACIÓN 1: Registrar cliente válido")
        try:
            c1 = sistema.registrar_cliente("001", "María López", "maria@email.com", "3101234567")
            print(f"✅ {c1}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n📌 OPERACIÓN 2: Registrar otro cliente válido")
        try:
            c2 = sistema.registrar_cliente("002", "Carlos Pérez", "carlos@email.com", "3209876543")
            print(f"✅ {c2}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n📌 OPERACIÓN 3: Intentar registrar cliente duplicado")
        try:
            c3 = sistema.registrar_cliente("001", "Duplicado", "duplicado@email.com", "1234567")
            print(f"✅ {c3}")
        except ClienteDuplicadoError as e:
            print(f"❌ Esperado: {e}")
        
        print("\n📌 OPERACIÓN 4: Intentar registrar cliente con correo inválido")
        try:
            c4 = sistema.registrar_cliente("004", "Correo Malo", "correo-sin-arroba", "1234567890")
            print(f"✅ {c4}")
        except DatoInvalidoError as e:
            print(f"❌ Esperado: {e}")
        
        print("\n📌 OPERACIÓN 5: Listar servicios disponibles")
        sistema.listar_servicios()
        
        print("\n📌 OPERACIÓN 6: Crear reserva — Reserva de Salas")
        try:
            r1 = sistema.crear_reserva("001", 0, 3)
            print(f"✅ Reserva creada exitosamente")
            print(f"   Costo sin impuesto: ${r1.calcular_total():,.2f}")
            print(f"   Costo con impuesto (19%): ${r1.calcular_total(impuesto=0.19):,.2f}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n📌 OPERACIÓN 7: Crear reserva — Alquiler de Equipos con descuento")
        try:
            r2 = sistema.crear_reserva("002", 1, 4)
            print(f"✅ Reserva creada exitosamente")
            print(f"   Costo sin descuento: ${r2.calcular_total(impuesto=0.19):,.2f}")
            print(f"   Costo con 10% descuento + impuesto: ${r2.calcular_total(impuesto=0.19, descuento=0.10):,.2f}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n📌 OPERACIÓN 8: Crear reserva — Asesoría Especializada")
        try:
            r3 = sistema.crear_reserva("001", 2, 2)
            print(f"✅ Reserva creada exitosamente")
            print(f"   Costo con impuesto: ${r3.calcular_total(impuesto=0.19):,.2f}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n📌 OPERACIÓN 9: Confirmar reserva")
        try:
            r1.confirmar()
            print(f"✅ Reserva confirmada. Estado actual: {r1.estado}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n📌 OPERACIÓN 10: Cancelar reserva")
        try:
            r2.cancelar()
            print(f"✅ Reserva cancelada. Estado actual: {r2.estado}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n📌 OPERACIÓN 11: Intentar cancelar una reserva ya completada (error esperado)")
        try:
            r2._estado = "COMPLETADA"
            r2.cancelar()
        except OperacionNoPermitidaError as e:
            print(f"❌ Esperado: {e}")
        
        print("\n📌 OPERACIÓN 12: Listar todas las reservas del sistema")
        sistema.listar_reservas()
        
        print("\n" + "=" * 60)
        print("   ✅ TODAS LAS PRUEBAS FINALIZADAS — Revisa el archivo logs.txt")
        print("=" * 60)


if _name_ == "_main_":
    app = SistemaReservas()
    app.ejecutar_pruebas()