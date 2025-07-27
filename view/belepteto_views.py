if not request.session.get('belepve'):
    return redirect('belepteto_view')


def belepteto_view(request):
    pontszam = None
    if request.method == 'POST':
        try:
            pontszam = sum(int(request.POST.get(q, 0)) for q in ['q1', 'q2', 'q3', 'q4'])
        except ValueError:
            pontszam = 0
        if pontszam >= 10:
            request.session['belepve'] = True  # vagy mentheted a user profilba
            return redirect('regisztracio_view')
        else:
            return render(request, 'belepteto.html', {'pontszam': pontszam, 'hiba': "Még nem ébredtél..."})
    return render(request, 'belepteto.html')
