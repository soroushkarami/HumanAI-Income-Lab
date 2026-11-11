from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .NeuralNet_Model.predictor import IncomePredictorModel
from .utils import person_picker
from .models import Scoreboard


def register_view(request):
    if request.method == 'POST':    # ie whether the user submitted the registration form
        form = UserCreationForm(request.POST)
        # create a form filled with the submitted data: username, password, password confirmation
        if form.is_valid():     # check submitted data: Is username unique?
                                # Do the two passwords match? Is the password secure enough?
            form.save()
            # creates a new user in the database

            return redirect('login')    # After registration succeeds, send the user to the login page
            # name 'login' is the built‑in URL name provided by:
            # path('accounts/', include('django.contrib.auth.urls'))
    else:
        form = UserCreationForm()   # create a blank form

    return render(request,
                  context= {'form': form},
                  template_name= 'registration/register.html')



the_model = None

@login_required     # a Django decorator that protects a view so that only logged‑in users can access it
# paths given in settings.py
def predict_view(request):
    global the_model
    if the_model is None:
        the_model = IncomePredictorModel()

    # TODO: GET --> show random person
    if request.method == 'GET':
        features_for_model, features_for_user, income = person_picker()

        # store in session for POST
        request.session['user_features'] = features_for_user
        request.session['model_features'] = features_for_model
        request.session['income'] = income

        return render(request,
                      context= {
                          'features': features_for_user,
                          'answer': None,
                          'human': None,
                          'ai': None
                      },
                      template_name='income_predictor/guessing_game.html')


    # TODO: POST --> submitted guess
    try:
        # Human guess
        human_guess = request.POST['human_guess']
    except MultiValueDictKeyError:
        return render(
            request,
            context= {'error': 'Invalid guess submission'},
            template_name= 'income_predictor/guessing_game.html'
        )

    round_num = Scoreboard.objects.filter(user=request.user).count() + 1
    # Scoreboard.objects.filter(user=request.user): Looks in the database
    # for all previous game rounds played by the currently logged‑in user

    # load stored person
    user_features = request.session.get('user_features')
    model_features = request.session.get('model_features')
    income = request.session.get('income')

    # AI prediction
    both_probs = the_model.predict(model_features)
    if both_probs[0][1] > both_probs[0][0]:
        ai_pred = '>50K'
        ai_prob = both_probs[0][1]
    else:
        ai_pred = '<=50K'
        ai_prob = both_probs[0][0]

    # save round's info as a new row into DB
    Scoreboard.objects.create(
        # user fields
        user = request.user,
        user_guess = human_guess,
        user_correct = (human_guess == income),

        # AI fields
        ai_guess = ai_pred,
        ai_confidence = ai_prob,
        ai_correct = (ai_pred == income),
        the_answer = income,

        round_num = round_num,

        # person fields
        age = user_features['Age'],
        workclass = user_features['Workclass'],
        education = user_features['Education'],
        marital_status = user_features['Marital Status'],
        occupation = user_features['Occupation'],
        relationship = user_features['Relationship'],
        race = user_features['Race'],
        sex = user_features['Sex'],
        hours_per_week = user_features['Hours Per Week'],
        native_country = user_features['Native Country'],
        capital_net = user_features['Capital Net'],
    )

    return render(request,
           context={
               'features': user_features,
               'answer': income,
               'human': f'Your Guess: {human_guess} --> {"CORRECT" if human_guess == income else "INCORRECT"}',
               'ai': f'AI: {ai_pred} with {(ai_prob*100):.2f}% confidence --> {"CORRECT" if ai_pred == income else "INCORRECT"}'
           },
           template_name='income_predictor/guessing_game.html')