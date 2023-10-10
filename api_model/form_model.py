form = {
    'config': {
        'id': 1
    },
    'data': [
        {
            'class': 'category',
            'title': 'my category',
            'children': [
                         {
                            'class': 'category',
                            'title': 'subcategory',
                            'children': [
                                {
                                   'class': 'tinymce',
                                   'description': 'test description',
                                   'children': [
                                              {
                                                  'class': 'object_model',
                                                  'description': 'test description',
                                                   'nameFields': [{
                                                       'type': 'text',
                                                       'value': '',
                                                   },
                                                 {
                                                       'type': 'number',
                                                       'value': '0',
                                                   },
                                                       {
                                                           'type': 'email',
                                                           'value': '@',
                                                       }

                                                   ],

                                                  'children': [{

                                                  }]
                                              }
                                            ]
                                }

                            ]
                         },
                       ]
        }
    ]
}