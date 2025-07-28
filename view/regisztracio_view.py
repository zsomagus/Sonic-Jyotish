
def regisztracio_view(request):
    if request.method == "POST":
        form = RegisztraciosForm(request.POST, request.FILES)
        if form.is_valid():
            # Először létrehozzuk a User-t
            user = User.objects.create_user(
                username=form.cleaned_data['email'],  # vagy máshonnan
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=User.objects.make_random_password()
            )

            # Majd a UserProfile-t
            generate_horoszkop_for_user(user)  # Te írod meg, és hozzárendeli a képet
            profile = UserProfile.objects.create(
                user=user,
                szuletesi_datum=form.cleaned_data['szuletesi_datum'],
                szuletesi_ido=form.cleaned_data['szuletesi_ido'],
                szuletesi_hely=form.cleaned_data['szuletesi_hely'],
                bemutatkozas=form.cleaned_data['bemutatkozas'],
                erdeklodes=form.cleaned_data['erdeklodes'],
                fenykep=form.cleaned_data['fenykep'],
            )

            login(request, user)
            return redirect('profil')
    else:
        form = RegisztraciosForm()
    return render(request, 'regisztracio.html', {'form': form})