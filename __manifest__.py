{
    'name':'Pharmacy Application',
    'category':'Application',
    'depends':['sale','sale_management','product','stock','account','sale_stock','point_of_sale'],
    'data':[
        'security/ir.model.access.csv',
        'security/security.xml',
        'view/medicine_feature.xml',
        'view/log_view.xml',
        'view/base_view.xml',
        ],
    'assets': {
            'point_of_sale.assets': [
                'pharmacy_application/static/src/js/pos_max_qty.js',
                        ],
            },
    'installable': True,
    'application': True,
    
}