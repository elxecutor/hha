from django.shortcuts import render
from django.contrib import messages
from kca_project.hymnal import get_hymn_text


def hymnal_home(request):
    """Display the hymnal search page"""
    return render(request, 'hymnal/hymnal.html')


def search_hymn(request):
    """Search for a hymn and display results"""
    hymn_text = None
    hymn_title = None
    search_query = ""

    if request.method == 'POST':
        search_query = request.POST.get('hymn_title', '').strip()

        if search_query:
            result = get_hymn_text(search_query)

            if result:
                hymn_text, hymn_title = result
                messages.success(request, f'Found hymn: {hymn_title.title()}')
            else:
                messages.error(request, f'Sorry, we couldn\'t find a hymn matching "{search_query}". Please try a different title.')
        else:
            messages.warning(request, 'Please enter a hymn title to search.')

    context = {
        'hymn_text': hymn_text,
        'hymn_title': hymn_title,
        'search_query': search_query,
    }

    return render(request, 'hymnal/hymnal.html', context)
