from .pdf_utils import generate_pdf_from_chart
from django.contrib.auth.decorators import login_required
from .pdf_utils import generate_ai_elemzes_pdf
from .astroai import astroai_valasz

@login_required
def letolt_pdf_view(request):
    return generate_pdf_from_chart(request.user)

@login_required
def astroai_pdf_view(request):
    kulcsszo = request.GET.get("kulcsszo", "Punarvasu")
    elemzes = astroai_valasz(kulcsszo)
    return generate_ai_elemzes_pdf(request.user.username, elemzes)
@login_required
def astroai_full_pdf_view(request):
    kulcsszo = request.GET.get("kulcsszo", "Punarvasu")
    elemzes = astroai_valasz(kulcsszo)

    # Planeták a user képletéből (pl. Poszt vagy profil alapján)
    planet_positions = user.userprofile.planet_positions
    purusharta_info = calculate_purusharta_distribution(planet_positions)

    return generate_full_report_pdf(request.user, elemzes, planet_positions, purusharta_info)
