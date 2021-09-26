from flask import render_template, request,redirect, url_for,abort
from . import main
from ..models import User, Blog,Comment
from .forms import BlogForm, CommentForm, UpdateProfile
from .. import db, photos
from flask_login import login_required,current_user


@main.route('/')
def index(): 
    # technology = Pitch.get_pitches('technology')
    # travels = Pitch.get_pitches('travels')
    # sports = Pitch.get_pitches('sports')
    
    return render_template('index.html')
    
# @main.route('/pitches/technology')
# def technology():
#     pitches = Pitch.get_pitches('technology')
    
#     return render_template('tech.html',pitches = pitches)

# @main.route('/pitches/travels')
# def travels():
#     pitches = Pitch.get_pitches('travels')
    
#     return render_template('travels.html', pitches = pitches)

# @main.route('/pitches/sports')
# def sports():
#     pitches = Pitch.get_pitches('sports')
    
#     return render_template('sports.html', pitches = pitches)

@main.route('/new/blog', methods = ['GET', 'POST'])
@login_required

def new_blog():
    blog_form = BlogForm()
    
    if log_form.validate_on_submit():
        title = blog_form.title.data
        blog = blog_form.text.data
        category = blog_form.category.data
        
        
        new_blog = Blog( body= title, content= Blog,  user = current_user, likes = 0, dislikes = 0)
        
        new_blog.save_blog()
        return redirect(url_for('.index'))
    
    title = 'new.blog'
    
    return render_template('newblog.html',title = title, blog_form = blog_form)

@main.route('/blog/<int:id>', methods=['GET','POST'])
@login_required

def blog(id):
    blog = Blog.get_blog(id)
    posted_date = blog.timestamp.strftime('%b %d,%Y')
    
    if request.args.get('likes'):
        blog.likes = blog.likes+1
        
        db.session.add(blog)
        db.session.commit()
        return redirect('/blog/{blog_id}'.format(blog_id = blog.id))

    elif request.args.get('dislikes'):
        blog.dislikes = blog.dislikes+1
        
        db.session.add(blog)
        db.session.commit()
        return redirect('/blog/{blog_id}'.format(blog_id = blog.id))
    
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.text.data   
        new_comment = Comment(comment = comment, user = current_user, blog_id = blog)
        new_comment.save_comments()
    
    comments = Comment.get_comments(blog)
    return render_template('action.html', blog = blog, comment_form = comment_form, comment = comments,date = posted_date )


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()
    
    if user is None:
        abort(404)
        
    return render_template("profile/profile.html", user = user)     


@main.route('/user/<uname>/update',methods =['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('.profile',uname = user.username))            
        
    return render_template('profile/update.html', form = form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))      