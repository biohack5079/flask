from flask import render_template, request, redirect, url_for, flash
from app import app
from models import db, Memo
from forms import MemoForm

# ============
# ルーティング
# ============

@app.route('/memo/')
def index():
    memos = Memo.query.all()
    return render_template('index.html', memos=memos)

@app.route('/memo/create/', methods=['GET', 'POST'])
def create():
    form = MemoForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        memo = Memo(title=title, content=content)
        db.session.add(memo)
        db.session.commit()
        flash('メモが作成されました。')
        return redirect(url_for('index'))
    # Get時
    # 画面遷移
    return render_template('create_form.html', form=form)


@app.route('/memo/update/<int:memo_id>', methods=['GET', 'POST'])
def update(memo_id):

    target_data = Memo.query.get_or_404(memo_id)
    form = MemoForm(obj=target_data)

    if request.method == 'POST' and form.validate():
        target_data.title = form.title.data
        target_data.content = form.content.data
        db.session.commit()
        flash('メモが更新されました。')
        return redirect(url_for('index'))
    return render_template('update_form.html', form=form, edit_id = target_data.id)

@app.route('/memo/delete/<int:memo_id>')
def delete(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    db.session.delete(memo)
    db.session.commit()
    flash('メモが削除されました。')
    return redirect(url_for('index'))

from werkzeug.exceptions import NotFound

@app.errorhandler(NotFound)
def show_404_page(error):
    msg = error.description
    print('エラー内容：', msg)
    return render_template('errors/404.html', msg=msg) , 404
