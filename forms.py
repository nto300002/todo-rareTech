from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, validators
from wtforms.fields import EmailField

class RegistrationForm(Form):
    username = StringField("名前", [validators.Length(min=3, max=64), validators.DataRequired()])
    email = EmailField("メールアドレス", [validators.Email(), validators.Length(max=64), validators.DataRequired()])
    password = PasswordField("パスワード", [validators.Length(min=8, max=128), validators.DataRequired(), validators.EqualTo("confirm", message="パスワードが一致しません")])
    confirm = PasswordField("確認パスワード")

