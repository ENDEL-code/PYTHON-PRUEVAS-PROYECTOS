import json
import os
from datetime import datetime
from collections import defaultdict

class ControlFinanciero:
    def __init__(self, archivo='finanzas.json'):
        self.archivo = archivo
        self.transacciones = []
        self.meta_ahorro = 10000
        self.categorias = {
            'gasto': ['Comida', 'Transporte', 'Entretenimiento', 'Servicios', 'Salud', 'Otros'],
            'ingreso': ['Salario', 'Freelance', 'Inversiones', 'Otros']
        }
        self.cargar_datos()
    
    def cargar_datos(self):
        """Carga los datos desde el archivo JSON"""
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self.transacciones = datos.get('transacciones', [])
                    self.meta_ahorro = datos.get('meta_ahorro', 10000)
            except:
                print("⚠️  Error al cargar datos. Iniciando con datos vacíos.")
    
    def guardar_datos(self):
        """Guarda los datos en el archivo JSON"""
        datos = {
            'transacciones': self.transacciones,
            'meta_ahorro': self.meta_ahorro
        }
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    
    def agregar_transaccion(self):
        """Agregar una nueva transacción"""
        print("\n" + "="*50)
        print("📝 NUEVA TRANSACCIÓN")
        print("="*50)
        
        # Tipo de transacción
        print("\n1. Ingreso")
        print("2. Gasto")
        tipo_opcion = input("\nSelecciona el tipo (1/2): ").strip()
        
        if tipo_opcion == '1':
            tipo = 'ingreso'
        elif tipo_opcion == '2':
            tipo = 'gasto'
        else:
            print("❌ Opción inválida")
            return
        
        # Descripción
        descripcion = input("\nDescripción: ").strip()
        if not descripcion:
            print("❌ La descripción no puede estar vacía")
            return
        
        # Monto
        try:
            monto = float(input("Monto: $").strip())
            if monto <= 0:
                print("❌ El monto debe ser mayor a 0")
                return
        except ValueError:
            print("❌ Monto inválido")
            return
        
        # Categoría
        print(f"\nCategorías de {tipo}:")
        categorias_tipo = self.categorias[tipo]
        for i, cat in enumerate(categorias_tipo, 1):
            print(f"{i}. {cat}")
        
        try:
            cat_opcion = int(input("\nSelecciona categoría: ").strip())
            if 1 <= cat_opcion <= len(categorias_tipo):
                categoria = categorias_tipo[cat_opcion - 1]
            else:
                print("❌ Opción inválida")
                return
        except ValueError:
            print("❌ Opción inválida")
            return
        
        # Crear transacción
        transaccion = {
            'id': len(self.transacciones) + 1,
            'tipo': tipo,
            'descripcion': descripcion,
            'monto': round(monto, 2),
            'categoria': categoria,
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.transacciones.append(transaccion)
        self.guardar_datos()
        print(f"\n✅ Transacción agregada exitosamente")
    
    def calcular_totales(self):
        """Calcula ingresos, gastos y balance"""
        ingresos = sum(t['monto'] for t in self.transacciones if t['tipo'] == 'ingreso')
        gastos = sum(t['monto'] for t in self.transacciones if t['tipo'] == 'gasto')
        balance = ingresos - gastos
        return ingresos, gastos, balance
    
    def ver_resumen(self):
        """Muestra el resumen financiero"""
        print("\n" + "="*50)
        print("💰 RESUMEN FINANCIERO")
        print("="*50)
        
        ingresos, gastos, balance = self.calcular_totales()
        
        print(f"\n{'Ingresos Totales:':<25} ${ingresos:>15,.2f}")
        print(f"{'Gastos Totales:':<25} ${gastos:>15,.2f}")
        print("-" * 50)
        print(f"{'Balance:':<25} ${balance:>15,.2f}")
        
        # Progreso de meta de ahorro
        if self.meta_ahorro > 0:
            progreso = (balance / self.meta_ahorro) * 100
            print(f"\n{'Meta de Ahorro:':<25} ${self.meta_ahorro:>15,.2f}")
            print(f"{'Progreso:':<25} {progreso:>15.1f}%")
            
            # Barra de progreso
            barra_longitud = 30
            progreso_barra = int((min(progreso, 100) / 100) * barra_longitud)
            barra = "█" * progreso_barra + "░" * (barra_longitud - progreso_barra)
            print(f"\n[{barra}]")
    
    def ver_gastos_por_categoria(self):
        """Muestra gastos agrupados por categoría"""
        print("\n" + "="*50)
        print("📊 GASTOS POR CATEGORÍA")
        print("="*50)
        
        gastos_cat = defaultdict(float)
        for t in self.transacciones:
            if t['tipo'] == 'gasto':
                gastos_cat[t['categoria']] += t['monto']
        
        if not gastos_cat:
            print("\nNo hay gastos registrados")
            return
        
        total_gastos = sum(gastos_cat.values())
        
        # Ordenar por monto descendente
        gastos_ordenados = sorted(gastos_cat.items(), key=lambda x: x[1], reverse=True)
        
        print(f"\n{'Categoría':<20} {'Monto':>12} {'Porcentaje':>12}")
        print("-" * 50)
        
        for categoria, monto in gastos_ordenados:
            porcentaje = (monto / total_gastos) * 100
            print(f"{categoria:<20} ${monto:>10,.2f} {porcentaje:>10.1f}%")
        
        print("-" * 50)
        print(f"{'TOTAL':<20} ${total_gastos:>10,.2f} {100:>10.1f}%")
    
    def ver_transacciones(self):
        """Muestra todas las transacciones"""
        print("\n" + "="*50)
        print("📜 HISTORIAL DE TRANSACCIONES")
        print("="*50)
        
        if not self.transacciones:
            print("\nNo hay transacciones registradas")
            return
        
        # Mostrar las últimas 20 transacciones
        transacciones_recientes = self.transacciones[-20:]
        transacciones_recientes.reverse()
        
        for t in transacciones_recientes:
            signo = "+" if t['tipo'] == 'ingreso' else "-"
            color = "🟢" if t['tipo'] == 'ingreso' else "🔴"
            print(f"\n{color} ID: {t['id']}")
            print(f"   {t['descripcion']}")
            print(f"   Categoría: {t['categoria']}")
            print(f"   Monto: {signo}${t['monto']:,.2f}")
            print(f"   Fecha: {t['fecha']}")
    
    def eliminar_transaccion(self):
        """Elimina una transacción por ID"""
        print("\n" + "="*50)
        print("🗑️  ELIMINAR TRANSACCIÓN")
        print("="*50)
        
        if not self.transacciones:
            print("\nNo hay transacciones para eliminar")
            return
        
        try:
            id_eliminar = int(input("\nIngresa el ID de la transacción a eliminar: ").strip())
            
            for i, t in enumerate(self.transacciones):
                if t['id'] == id_eliminar:
                    confirmacion = input(f"\n¿Eliminar '{t['descripcion']}' (${t['monto']:.2f})? (s/n): ").strip().lower()
                    if confirmacion == 's':
                        self.transacciones.pop(i)
                        self.guardar_datos()
                        print("✅ Transacción eliminada")
                    else:
                        print("❌ Operación cancelada")
                    return
            
            print("❌ ID no encontrado")
        except ValueError:
            print("❌ ID inválido")
    
    def establecer_meta_ahorro(self):
        """Establece una nueva meta de ahorro"""
        print("\n" + "="*50)
        print("🎯 META DE AHORRO")
        print("="*50)
        
        print(f"\nMeta actual: ${self.meta_ahorro:,.2f}")
        
        try:
            nueva_meta = float(input("\nNueva meta de ahorro: $").strip())
            if nueva_meta <= 0:
                print("❌ La meta debe ser mayor a 0")
                return
            
            self.meta_ahorro = round(nueva_meta, 2)
            self.guardar_datos()
            print(f"✅ Meta establecida en ${self.meta_ahorro:,.2f}")
        except ValueError:
            print("❌ Monto inválido")
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        print("\n" + "="*50)
        print("💰 CONTROL DE GASTOS Y AHORROS")
        print("="*50)
        print("\n1. Agregar transacción")
        print("2. Ver resumen financiero")
        print("3. Ver gastos por categoría")
        print("4. Ver historial de transacciones")
        print("5. Eliminar transacción")
        print("6. Establecer meta de ahorro")
        print("7. Salir")
        print("\n" + "="*50)
    
    def ejecutar(self):
        """Ejecuta el programa principal"""
        while True:
            self.mostrar_menu()
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == '1':
                self.agregar_transaccion()
            elif opcion == '2':
                self.ver_resumen()
            elif opcion == '3':
                self.ver_gastos_por_categoria()
            elif opcion == '4':
                self.ver_transacciones()
            elif opcion == '5':
                self.eliminar_transaccion()
            elif opcion == '6':
                self.establecer_meta_ahorro()
            elif opcion == '7':
                print("\n✅ ¡Gracias por usar el sistema! Adiós.")
                break
            else:
                print("\n❌ Opción inválida. Intenta de nuevo.")
            
            input("\nPresiona Enter para continuar...")

# Ejecutar el programa
if __name__ == "__main__":
    control = ControlFinanciero()
    control.ejecutar()