from wtforms import Form, StringField, TextAreaField, PasswordField, DateField, validators
from wtforms.fields import EmailField

class RegistrationForm(Form):
    username = StringField("名前", [validators.Length(min=3, max=64), validators.DataRequired()])
    email = EmailField("メールアドレス", [validators.Email(), validators.Length(max=64), validators.DataRequired()])
    password = PasswordField("パスワード", [validators.Length(min=8, max=128), validators.DataRequired(), validators.EqualTo("confirm", message="パスワードが一致しません"), validators.Regexp('^((?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])|(?=.*[a-z])(?=.*[A-Z])(?=.*[!@;:])|(?=.*[A-Z])(?=.*[0-9])(?=.*[!@;:])|(?=.*[a-z])(?=.*[0-9])(?=.*[!@;:]))([a-zA-Z0-9!@;:]){8,}$', message='英大文字・英小文字・数字・パスワードの4種類  のうち3種類以上を使ってパスワードを作成してください')])
    confirm = PasswordField("確認パスワード")

class TaksForm(Form):
    title = StringField("タイトル", [validators.Length(min=5, max=64), validators.DataRequired()])
    detail = TextAreaField("内容", [validators.Length(min=8, max=128), validators.DataRequired()])
    end_time = DateField("期限", format='%Y/%m/%d')
