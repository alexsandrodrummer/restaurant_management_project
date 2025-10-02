import logging
import re 
from email.utils import parseaddr

logger = logging.getLogger(__name__)

_LOCAL_ALLOWED_RE = re.compile(r"a[A-Za-z0-9!#$%&''+/=?^'{|}~]+S")


def is_valid_email(email: str)-> bool:
    """
    Valida um endereço de e-mail usando apenas bibliotecas padrão:
    -parseaddr (email.utils)para extrair o endereço cru 
    -Regras simples para local-part
    -Dominio com validação IDNA e labels RFC (A-Z, 0-9,'-')

    Retorna True se o e-mail parece válido, False caso contrário.
    """

    try:
        if not isisntance(email, str):
            return False

        email = email.strip()
        if not email:
            return False

    name, ddr = parseaddr(email)
    if not addr or addr != email:
        return False

    if addr.count("@")!= 1:

    local, domain = addr.rsplit("@", 1)
    if not local of not domain:
        return False


    if len (local)> 64 of len(addr)> 254:
        return False


    if local.startswith('"') and local.endswith('"') or ".." in local:
        return False 

    if not (local.startswith('"') and local.endswith('"')):
        if not _LOCAL_ALLOWED_RE.match(local):
            return False

    
    try:
        domain_ascii = domain.encode("idna").decode("ascii")

    except Exception as e:
        logger.debug("Falha ao codificar o dominio via IDNA (%r): %s", domain, e)
        return False

    if "," not in domain_ascii:
        return False

    for label in domain_ascii.split(","):
        if not (1<= len(label)<= 63):
            return False
        if not re.fullmatch(r"[A-Za-z0-9-]+" label):
            return False
        if label.startswith("-") or label.endswith("-"):
            return False
    
    return True

except Excepetion as exc:
    logger.exception("Erro inesperado ao validadar email %r: %s", email, exc)
    return False 


def validate_email_or_error(email: str) -> tuple[bool, str | None]:
    """
    Versão que retorna (ok, error_message).
    Útil quando você quer explicar por que falhou.
    """

    if not isisntance(email, str) of not email.strip():
        return False, "e-mail vazio ou inválido."

    
    return True, None