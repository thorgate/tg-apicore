COMPANIES_DATA = {
    "type": "company",
    "id": "12",
    "attributes": {
        "created": "2018-02-21T14:55:06.734781Z",
        "name": "Turner and Sons",
        "email": "turner@sons.com"
    },
    "relationships": {
        "employees": {
            "meta": {
                "count": 2
            },
            "data": [
                {
                    "type": "employment",
                    "id": "91"
                },
                {
                    "type": "employment",
                    "id": "162"
                }
            ]
        }
    },
    "links": {
        "self": "%(API_ROOT)s/companies/12/"
    }
}

COMPANIES_LIST_RESPONSE = {
    "links": {
        "next": "%(API_ROOT)s/companies/?cursor=cD0yMDE3LTA5LTIyKzA4JTNBMzklM0EyNS4wMDIxNTIlMkIwMCUzQTAw",
        "prev": None
    },
    "data": [
        {
            "type": "company",
            "id": "12",
            "attributes": {
                "created": "2018-02-21T14:55:06.734781Z",
                "name": "Turner and Sons",
                "email": "turner@sons.com"
            },
            "relationships": {
                "employees": {
                    "meta": {
                        "count": 3
                    },
                    "data": [
                        {
                            "type": "employment",
                            "id": "91"
                        },
                        {
                            "type": "employment",
                            "id": "162"
                        }
                    ]
                }
            },
            "links": {
                "self": "%(API_ROOT)s/companies/12/"
            }
        }
    ],
    "included": [
        {
            "type": "employment",
            "id": "162",
            "attributes": {
                "created": "2018-02-21T14:55:06.756900Z",
                "name": "Linda Burgess",
                "email": "carloswoods@griffin.com",
                "role": 1
            },
            "links": {
                "self": "%(API_ROOT)s/employments/162/"
            }
        },
        {
            "type": "employment",
            "id": "91",
            "attributes": {
                "created": "2018-02-21T14:55:06.755331Z",
                "name": "Crystal Turner",
                "email": "collinsheather@mendoza.biz",
                "role": 1
            },
            "links": {
                "self": "%(API_ROOT)s/employments/91/"
            }
        }
    ]
}

COMPANIES_CREATE_REQUEST = {
    "data": {
        "type": "company",
        "attributes": {
            "name": "Turner and Sons",
            "email": "turner@sons.com"
        }
    }
}

COMPANIES_CREATE_RESPONSE = {
    "data": {
        "type": "company",
        "id": "12",
        "attributes": {
            "created": "2018-02-21T14:55:06.734781Z",
            "name": "Turner and Sons",
            "email": "turner@sons.com"
        },
        "links": {
            "self": "%(API_ROOT)s/companies/12/"
        }
    },
}

COMPANIES_CREATE_RESPONSES = [
    (201, COMPANIES_CREATE_RESPONSE),
    (400, {
        "errors": [
            {
                "detail": "Company with this name already exists.",
                "source": {
                    "pointer": "/data/attributes/name"
                },
                "status": "400"
            }
        ]
    }),
]

COMPANIES_READ_RESPONSE = {
    "data": {
        "type": "company",
        "id": "12",
        "attributes": {
            "created": "2018-02-21T14:55:06.734781Z",
            "name": "Turner and Sons",
            "email": "turner@sons.com"
        },
        "relationships": {
            "employees": {
                "meta": {
                    "count": 3
                },
                "data": [
                    {
                        "type": "employment",
                        "id": "91"
                    },
                    {
                        "type": "employment",
                        "id": "162"
                    }
                ]
            }
        },
        "links": {
            "self": "%(API_ROOT)s/companies/70/"
        }
    },
    "included": [
        {
            "type": "employment",
            "id": "162",
            "attributes": {
                "created": "2018-02-21T14:55:06.756900Z",
                "name": "Linda Burgess",
                "email": "carloswoods@griffin.com",
                "role": 1
            },
            "links": {
                "self": "%(API_ROOT)s/employments/162/"
            }
        },
        {
            "type": "employment",
            "id": "91",
            "attributes": {
                "created": "2018-02-21T14:55:06.755331Z",
                "name": "Crystal Turner",
                "email": "collinsheather@mendoza.biz",
                "role": 1
            },
            "links": {
                "self": "%(API_ROOT)s/employments/91/"
            }
        }
    ]
}

COMPANIES_UPDATE_REQUEST = {
    "data": {
        "type": "company",
        "id": "12",
        "attributes": {
            "name": "Turner and Sons"
        }
    }
}

COMPANIES_DELETE_RESPONSES = [
    (204, None),
    (400, {
        "errors": [
            {
                "detail": "This company cannot be deleted",
                "source": {
                    "pointer": "/data"
                },
                "status": "400"
            }
        ]
    }),
]
