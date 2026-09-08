class TransicionInvalidaError(Exception):
    """Se intentó mover una inscripción a un estado que no le corresponde."""


class LimiteCreditosError(Exception):
    """El estudiante ya alcanzó los créditos ACOM requeridos para titularse."""
