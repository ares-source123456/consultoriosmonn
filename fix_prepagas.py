"""
Script para corregir suscripciones existentes que fueron aprobadas
pero no tienen el pago del mes actual como APROBADO.

Ejecutar con: python fix_existing_subscriptions.py
"""

from datetime import datetime, date
from calendar import monthrange
from app import app, db
from models_prepaga import (SuscripcionPrepaga, PagoMensualPrepaga, 
                            EstadoSuscripcion, EstadoPagoMensual)

def fix_existing_subscriptions():
    """
    Busca suscripciones ACTIVAS que no tienen pago del mes actual aprobado
    y crea el pago correspondiente.
    """
    with app.app_context():
        hoy = date.today()
        
        # Buscar suscripciones activas
        suscripciones_activas = SuscripcionPrepaga.query.filter_by(
            estado=EstadoSuscripcion.ACTIVA
        ).all()
        
        corregidas = 0
        
        for suscripcion in suscripciones_activas:
            # Verificar si tiene pago del mes actual
            pago_mes_actual = PagoMensualPrepaga.query.filter_by(
                suscripcion_id=suscripcion.id,
                mes=hoy.month,
                anio=hoy.year,
                estado=EstadoPagoMensual.APROBADO
            ).first()
            
            if not pago_mes_actual:
                # No tiene pago del mes actual aprobado, crear uno
                print(f"Corrigiendo suscripción ID {suscripcion.id} - Usuario: {suscripcion.usuario.nombre} {suscripcion.usuario.apellido}")
                
                ultimo_dia = monthrange(hoy.year, hoy.month)[1]
                fecha_venc = date(hoy.year, hoy.month, min(10, ultimo_dia))
                
                # Verificar si existe un pago pendiente del mes actual
                pago_pendiente = PagoMensualPrepaga.query.filter_by(
                    suscripcion_id=suscripcion.id,
                    mes=hoy.month,
                    anio=hoy.year
                ).first()
                
                if pago_pendiente:
                    # Si existe pero no está aprobado, aprobarlo
                    pago_pendiente.estado = EstadoPagoMensual.APROBADO
                    pago_pendiente.fecha_aprobacion = datetime.utcnow()
                    pago_pendiente.observaciones = "Corregido automáticamente - Suscripción ya estaba activa"
                    print(f"  -> Pago existente actualizado a APROBADO")
                else:
                    # Crear nuevo pago aprobado
                    nuevo_pago = PagoMensualPrepaga(
                        suscripcion_id=suscripcion.id,
                        mes=hoy.month,
                        anio=hoy.year,
                        monto=suscripcion.plan.precio_mensual,
                        fecha_vencimiento=fecha_venc,
                        estado=EstadoPagoMensual.APROBADO,
                        fecha_aprobacion=datetime.utcnow(),
                        observaciones="Creado automáticamente - Suscripción ya estaba activa"
                    )
                    db.session.add(nuevo_pago)
                    print(f"  -> Nuevo pago creado como APROBADO")
                
                corregidas += 1
        
        if corregidas > 0:
            db.session.commit()
            print(f"\n✅ {corregidas} suscripciones corregidas exitosamente")
        else:
            print("\n✅ No hay suscripciones que necesiten corrección")

if __name__ == '__main__':
    fix_existing_subscriptions()
