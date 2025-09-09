import shutil
import os
from datetime import datetime
import json
from models import *
from app import db

class BackupManager:
    """مدير النسخ الاحتياطي للبيانات"""
    
    def __init__(self, backup_dir='backup'):
        self.backup_dir = backup_dir
        self.ensure_backup_dir()
    
    def ensure_backup_dir(self):
        """التأكد من وجود مجلد النسخ الاحتياطية"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_database_backup(self):
        """إنشاء نسخة احتياطية من قاعدة البيانات"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # نسخ ملف قاعدة البيانات
            db_source = 'data/printing_costs.db'
            db_backup = f'{self.backup_dir}/db_backup_{timestamp}.db'
            
            if os.path.exists(db_source):
                shutil.copy2(db_source, db_backup)
                
                # إنشاء ملف معلومات عن النسخة الاحتياطية
                backup_info = {
                    'backup_date': datetime.now().isoformat(),
                    'database_file': db_backup,
                    'backup_type': 'database',
                    'file_size': os.path.getsize(db_backup),
                    'original_path': db_source
                }
                
                info_file = f'{self.backup_dir}/backup_info_{timestamp}.json'
                with open(info_file, 'w', encoding='utf-8') as f:
                    json.dump(backup_info, f, ensure_ascii=False, indent=2)
                
                return {
                    'success': True,
                    'backup_file': db_backup,
                    'info_file': info_file,
                    'timestamp': timestamp
                }
            else:
                return {
                    'success': False,
                    'error': 'لم يتم العثور على ملف قاعدة البيانات'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'خطأ في إنشاء النسخة الاحتياطية: {str(e)}'
            }
    
    def create_data_export(self):
        """تصدير البيانات إلى ملف JSON"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            export_file = f'{self.backup_dir}/data_export_{timestamp}.json'
            
            # جمع البيانات من جميع الجداول
            data_export = {
                'export_date': datetime.now().isoformat(),
                'academic_years': [],
                'subjects': [],
                'books': [],
                'printing_prices': [],
                'addons': [],
                'employees': [],
                'orders': []
            }
            
            # تصدير السنوات الدراسية
            for year in AcademicYear.query.all():
                data_export['academic_years'].append({
                    'id': year.id,
                    'name': year.name,
                    'description': year.description,
                    'is_active': year.is_active
                })
            
            # تصدير المواد
            for subject in Subject.query.all():
                data_export['subjects'].append({
                    'id': subject.id,
                    'name': subject.name,
                    'academic_year_id': subject.academic_year_id,
                    'is_active': subject.is_active
                })
            
            # تصدير الكتب
            for book in Book.query.all():
                data_export['books'].append({
                    'id': book.id,
                    'name': book.name,
                    'pages': book.pages,
                    'subject_id': book.subject_id,
                    'is_active': book.is_active
                })
            
            # تصدير أسعار الطباعة
            for price in PrintingPrice.query.all():
                data_export['printing_prices'].append({
                    'id': price.id,
                    'name': price.name,
                    'price_per_page': float(price.price_per_page),
                    'description': price.description,
                    'is_active': price.is_active
                })
            
            # تصدير الإضافات
            for addon in AddOn.query.all():
                data_export['addons'].append({
                    'id': addon.id,
                    'name': addon.name,
                    'price': float(addon.price),
                    'description': addon.description,
                    'is_active': addon.is_active
                })
            
            # تصدير الموظفين (بدون كلمات المرور)
            for employee in Employee.query.all():
                data_export['employees'].append({
                    'id': employee.id,
                    'username': employee.username,
                    'name': employee.name,
                    'role': employee.role,
                    'is_active': employee.is_active,
                    'created_at': employee.created_at.isoformat() if employee.created_at else None
                })
            
            # تصدير الطلبات
            for order in Order.query.all():
                data_export['orders'].append({
                    'id': order.id,
                    'order_number': order.order_number,
                    'customer_name': order.customer_name,
                    'customer_phone': order.customer_phone,
                    'status': order.status,
                    'total_cost': float(order.total_cost),
                    'created_at': order.created_at.isoformat() if order.created_at else None,
                    'completed_at': order.completed_at.isoformat() if order.completed_at else None
                })
            
            # حفظ البيانات
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(data_export, f, ensure_ascii=False, indent=2)
            
            return {
                'success': True,
                'export_file': export_file,
                'timestamp': timestamp,
                'records_count': {
                    'academic_years': len(data_export['academic_years']),
                    'subjects': len(data_export['subjects']),
                    'books': len(data_export['books']),
                    'printing_prices': len(data_export['printing_prices']),
                    'addons': len(data_export['addons']),
                    'employees': len(data_export['employees']),
                    'orders': len(data_export['orders'])
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'خطأ في تصدير البيانات: {str(e)}'
            }
    
    def get_backup_list(self):
        """الحصول على قائمة النسخ الاحتياطية"""
        try:
            backups = []
            
            if not os.path.exists(self.backup_dir):
                return backups
            
            for filename in os.listdir(self.backup_dir):
                filepath = os.path.join(self.backup_dir, filename)
                if os.path.isfile(filepath):
                    file_info = {
                        'filename': filename,
                        'filepath': filepath,
                        'size': os.path.getsize(filepath),
                        'created_at': datetime.fromtimestamp(os.path.getctime(filepath)),
                        'type': 'database' if filename.endswith('.db') else 'export' if filename.endswith('.json') else 'info'
                    }
                    backups.append(file_info)
            
            # ترتيب حسب التاريخ (الأحدث أولاً)
            backups.sort(key=lambda x: x['created_at'], reverse=True)
            return backups
            
        except Exception as e:
            return []
    
    def delete_backup(self, filename):
        """حذف نسخة احتياطية"""
        try:
            filepath = os.path.join(self.backup_dir, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                return {'success': True, 'message': 'تم حذف النسخة الاحتياطية بنجاح'}
            else:
                return {'success': False, 'error': 'الملف غير موجود'}
        except Exception as e:
            return {'success': False, 'error': f'خطأ في حذف الملف: {str(e)}'}
    
    def create_full_backup(self):
        """إنشاء نسخة احتياطية كاملة (قاعدة البيانات + تصدير البيانات)"""
        db_result = self.create_database_backup()
        export_result = self.create_data_export()
        
        return {
            'database_backup': db_result,
            'data_export': export_result,
            'success': db_result.get('success', False) and export_result.get('success', False)
        }