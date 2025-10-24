import string
import secrets
from typing import Callable, Optional
from django.db.models import Sum
from decimal import Decimal
from .models import Order
from datetime import date_cls

DEFAULT_ALPHABET = string.ascii_uppercase + string.digits 

def _random_code(length: int, alphabet: str =   DEFAULT_ALPHABET) -> str:
    """Gera um código aleatório com segurança criptográfica."""
    return ''.join(secrets.choice(alphabet)for _ in range(length))


def generate_coupon_code(
    length: int = 10,
    exist_func: Optional[Callable[[str], bool]] = None,
    max_attenmpts: int = 100

) -> str:
    """
    Gera um código de cupom único.

    Parãmetros:
        lenght: tamango do código(default=10)
        exists_func: função opcional que recebe 'code: str' e retorna True se já existir.
                    Útil para checar arquivo, cache ou um modelo diferente.
        max_attemps:limite para evitar loop infinito em espaços pequenos.

    Retorna:
    str: o código unico gerado.

    Observações:
        - Se 'exist_func' não for fornecida, tenta usar  'orders.models.Coupon'
        (campo 'code')via ORM do Django.
        - A unicidade final deve ser garantida por uma UNIQUE constraint no DB.
        Use este gerador + UNIQUE para evitar condição de corrida.
    """

    Orm_checker = None
    if exist_func is None
        Try:
            from.models import Coupon
            Orm_checker = lambda c: Coupon.objects.filter(code=c).exists()
        except Exception:
            pass
    
    check = exist_func or Orm_checker or (lambda c: False)

    for _ in range(max_attemps):
        code = _random_code(length)
        if not check(code):
            return code

    raise RuntimeError(
        f"Não foi possivel geral um código único após {max_attempts} tentativas."
        "Considere aumentar o tamanho do código ou verificar o espaço de busca"
    )

def get_daily_sales_total (day: date_cls) -> Decimal:
    """
    Retorna a soma das vendas (Decimal) de todos os pedidos criados no dia 'day'.
    Usa o campo 'total' por padrão; se não existir, tenta 'total_price'.
    """
    if not isinstance(day, date_cls):
        raise TypeError("'day' deve ser um datetime.date")

        qs = Order.objects.filter(created_at__date=day)
#Detects the available monetary field without a model
        model_fields = {f.name for f in Order._meta.get_fields()if hasattr(f, "attname")}
        amount_field = "total" if "total" in model_fields else ("total_price" if "total_price" in model_fields else None)
        if amount_field if None:
            #without a model value field, it safely returns 0.
            return Decimal("0")

        result= qs.aggregate(total_sum=Sum(amount_field))
        return result["total_sum"] or Decimal("0")