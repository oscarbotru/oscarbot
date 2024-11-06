
def mock_yaml_load(*args, **kwargs):
    return {
        'messages': {
            'start': '\' Hello! \'',
            'args': '\' Hello! {1}, {2} \''
        },
        'defaults': {
            'text_processor': '\'  \'',
            'dont_know': '\'Sorry, i do not know this command\'',
            'voice_processor': '\'  \''
        }
    }

