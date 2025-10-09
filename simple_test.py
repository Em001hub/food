from flask import Flask, render_template_string

app = Flask(__name__)
app.secret_key = 'test_key'

template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Test</title>
</head>
<body>
    <h1>Test Page</h1>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
</body>
</html>
'''

@app.route('/')
def test():
    return render_template_string(template)

if __name__ == '__main__':
    app.run(debug=True)