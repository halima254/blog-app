from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import required, Required


class BlogForm(FlaskForm):
    title = StringField('blog_title')
    text = TextAreaField('blog_text')
    # category = SelectField('pitch_type', choices=[('technology','Tech-Pitch'), ('travels', 'Travels-Pitch'),('sports', 'Sports-Pitch')])
    submit = SubmitField('submit')


class CommentForm(FlaskForm):
    text = TextAreaField('yoursay')
    submit = SubmitField('submit')
    
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you',validators=[Required()])
    
    submit = SubmitField('Submit')
        