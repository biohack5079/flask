from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from models import Memo


class MemoForm(FlaskForm):
    title = StringField('タイトル', validators=[DataRequired('タイトルを入力してください。'), Length(max=10, message='10文字以内で入力してください。')])
    content = TextAreaField('本文:')
    submit = SubmitField('送信')

    def validate_title(self, title):
        memo = Memo.query.filter_by(title=title.data).first()
        if memo:
            raise ValidationError(f"タイトル '{title.data}' は既に使用されています。\
                                    別のタイトルを入力してください。")