from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import Required

class ReigsterForm(FlaskForm):
    telephone = StringField('手机号码', validators=[Required()])
    username = StringField('用户名', validators=[Required()])
    password = PasswordField('密码', validators=[Required()])
    confirmpassword = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('确认注册')

class LoginForm(FlaskForm):
    telephone = StringField('手机号码', validators=[Required()])
    password = PasswordField('密码', validators=[Required()])
    submit = SubmitField('登陆')

class ArticleForm(FlaskForm):
    title = StringField('标题', validators=[Required()])
    content = TextAreaField('内容', validators=[Required()])
    submit = SubmitField('发布')

class InfoForm(FlaskForm):
    email = StringField('邮箱：')
    address = StringField('地址：')
    hobby = TextAreaField('兴趣爱好：')
    submit = SubmitField('提交信息')