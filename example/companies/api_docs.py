COMPANIES_DATA = {
    "type": "company",
    "id": "12",
    "attributes": {
        "created": "2018-03-16T09:38:01.531816Z",
        "updated": "2018-03-16T09:38:01.531879Z",
        "reg_code": "287-0513",
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
                "created": "2018-03-16T09:38:01.531816Z",
                "updated": "2018-03-16T09:38:01.531879Z",
                "reg_code": "287-0513",
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
    ],
    "included": [
        {
            "type": "employment",
            "id": "162",
            "attributes": {
                "created": "2018-03-16T09:48:11.528352Z",
                "updated": "2018-03-16T09:48:11.528494Z",
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
                "created": "2018-03-16T09:48:11.528352Z",
                "updated": "2018-03-16T09:48:11.528494Z",
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
            "reg_code": "123-4567",
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
            "created": "2018-03-16T09:38:01.531816Z",
            "updated": "2018-03-16T09:38:01.531879Z",
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
                "detail": "Company with this reg_code already exists.",
                "source": {
                    "pointer": "/data/attributes/reg_code"
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
            "created": "2018-03-16T09:38:01.531816Z",
            "updated": "2018-03-16T09:38:01.531879Z",
            "reg_code": "287-0513",
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
    },
    "included": [
        {
            "type": "employment",
            "id": "162",
            "attributes": {
                "created": "2018-03-16T09:48:11.528352Z",
                "updated": "2018-03-16T09:48:11.528494Z",
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
                "created": "2018-03-16T09:48:11.528352Z",
                "updated": "2018-03-16T09:48:11.528494Z",
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


EMPLOYMENTS_DATA = {
    "type": "employment",
    "id": "162",
    "attributes": {
        "created": "2018-03-16T09:48:11.528352Z",
        "updated": "2018-03-16T09:48:11.528494Z",
        "name": "Linda Burgess",
        "email": "carloswoods@griffin.com",
        "role": 1
    },
    "relationships": {
        "company": {
            "data": {
                "type": "company",
                "id": "12"
            }
        }
    },
    "links": {
        "self": "%(API_ROOT)s/employments/162/"
    }
}

EMPLOYMENTS_CREATE_REQUEST = {
    "data": {
        "type": "employment",
        "attributes": {
            "email": "carloswoods@griffin.com",
        },
        "relationships": {
            "company": {
                "data": {"type": "company", "id": "12"}
            }
        }
    }
}

EMPLOYMENTS_CREATE_RESPONSE = {
    "data": {
        "type": "employment",
        "id": "162",
        "attributes": {
            "created": "2018-03-16T09:48:11.528352Z",
            "updated": "2018-03-16T09:48:11.528494Z",
            "name": "Linda Burgess",
            "email": "carloswoods@griffin.com",
            "role": 1
        },
        "relationships": {
            "company": {
                "data": {
                    "type": "company",
                    "id": "12"
                }
            }
        },
        "links": {
            "self": "%(API_ROOT)s/employments/162/"
        }
    },
    "included": [
        {
            "type": "company",
            "id": "12",
            "attributes": {
                "created": "2018-03-16T09:38:01.531816Z",
                "updated": "2018-03-16T09:38:01.531879Z",
                "reg_code": "287-0513",
                "name": "Turner and Sons",
                "email": "turner@sons.com"
            },
            "links": {
                "self": "http://localhost:8330/api/2018-02-21/companies/12"
            }
        }
    ]
}

EMPLOYMENTS_CREATE_RESPONSES = [
    (201, EMPLOYMENTS_CREATE_RESPONSE),
    (400, {
        "errors": [
            {
                "detail": "You are not admin in the specified company",
                "source": {
                    "pointer": "/data/attributes/company"
                },
                "status": "400"
            }
        ]
    }),
]
