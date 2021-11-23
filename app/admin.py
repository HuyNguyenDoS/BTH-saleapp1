from flask_admin.contrib.sqla import ModelView
from app.model import Category, Product, Tag, User, UserRole
from app import db, admin, app
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect

class ProuctView(AdminAuthenticatedView):
    can_view_details = True
    can_export = True
    edit_modal = True
    column_filters = ['name', 'price', 'category']              #tìm kiếm theo []


class AdminAuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

#xem ki lai
class Logout_View(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()

        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(AdminAuthenticatedView(Category, db.session))
admin.add_view(ProuctView(Product, db.session))
admin.add_view(AdminAuthenticatedView(Tag, db.session))
admin.add_view(AdminAuthenticatedView(User, db.session, name='Nguoi dung'))
admin. add_view(Logout_View(name='Dang Xuat'))


#flask admin localization(địa phương hóa)
# + pip install flask-babelex