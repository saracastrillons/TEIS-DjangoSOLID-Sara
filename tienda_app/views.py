from django.shortcuts import render
from django.views import View

from .infra.factories import PaymentFactory
from .services import CompraService


class CompraView(View):
    template_name = 'tienda_app/compra.html'

    def setup_service(self): return CompraService(procesador_pago=PaymentFactory.get_processor())

    def get(self, request, libro_id): return render(request, self.template_name, self.setup_service().obtener_detalle_producto(libro_id))

    def post(self, request, libro_id):
        try: total = self.setup_service().ejecutar_compra(libro_id, cantidad=1)
        except Exception as e: return render(request, self.template_name, {'error': str(e)}, status=400)
        return render(request, self.template_name, {'mensaje_exito': f"¡Gracias por su compra! Total: ${total:.2f}", 'total': total})