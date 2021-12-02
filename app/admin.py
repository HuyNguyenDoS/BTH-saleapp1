from flask_admin.contrib.sqla import ModelView
from app.model import Category, Product, Tag, User, UserRole
from app import db, admin, app, utils
from flask_admin import BaseView, expose, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect
from flask_admin import Admin


class AdminAuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class ProductView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    column_exclude_list = ['image', 'active', 'created_date']
    column_labels = {
        'name': 'Ten SP',
        'description': 'Mo ta',
        'price': 'Gia',
        'image': 'Anh dai dien',
        'category': 'Danh muc'
    }
    column_sortable_list = ['id', 'name', 'price']            #tìm kiếm theo []

#xem ki lai
class Logout_View(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()

        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=utils.category_stats())

admin = Admin(app=app, name="Saleapp", template_mode="bootstrap4", index_view=MyAdminIndex())


# admin.add_view(AdminAuthenticatedView(Category, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(User, db.session, name='Nguoi dung'))
admin.add_view(Logout_View(name='Dang Xuat'))


#flask admin localization(địa phương hóa)
# + pip install flask-babelex