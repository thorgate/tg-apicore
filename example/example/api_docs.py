# API docs, shown on interactive docs page

"""
# Example API

The Example API is organized around REST.
Our API has predictable, resource-oriented URLs, and uses HTTP response codes to indicate API errors.
We use built-in HTTP features, like HTTP authentication and HTTP verbs,
which are understood by off-the-shelf HTTP clients.
JSON is returned by all API responses, including errors.

All request data must use UTF-8 encoding.

All dates and timestamps must be in extended ISO-8601 format and response data uses UTC timezone.
Examples of valid inputs:

- `2017-10-01T12:34:56.123456Z`
- `2017-10-01T12:34:56Z`
- `2017-10-01T14:34Z`
- `2017-10-01T14:34:56+02:00`
- `2017-10-01T14:34:56`

If timezone isn't given, it defaults to UTC.
Response data is always in extended ISO-8601 format, e.g. `2017-10-01T12:34:56.123456Z` or `2017-10-01T12:34:56Z`.


## Access & endpoints

All current Example API endpoints have `%(API_ROOT)s/` URL prefix.


## JSON API

Example API is built using principles of [JSON API standard](http://jsonapi.org/format/).
We chose JSON API because it provides a standard data exchange format that is real-world tested and fits our usecase.
As an example, it provides a standardized way of including subresources, such as employments,
when data of e.g. a company object is requested.

In short, every response body is a JSON object, containing at least either `data` (for successful requests)
or `errors` (for failed ones).
`data` is either a single resource object (in case a single resource was requested) or
a list of resource objects (in case a listing was requested).

Each resource has `id` and `type` and usually `attributes` which is a JSON object containing resource's data (fields).

Response can also contain `included` top-level key, which is a list of related resources. This is used to e.g. include
all `employment` resources when a `company` is requested, so that the client wouldn't have to request the employments
separately.

An example response to a request for a single `company` follows:

    :::json
    {
        "data": {
            "type": "company",
            "id": "113",
            "attributes": {
                "name": "Turner and Sons",
                "email": "turner@sons.com"
            },
            "links": {
                "self": "%(API_ROOT)s/companies/113/"
            }
        }
    }


## Pagination

List responses are paginated using cursor-paged pagination. The response include `next` and `previous` keys which are
links to the next/previous page of results, or `null` if there is no next/previous page.

20 results are returned per page by default but you shouldn't rely on this.
The number of results per page can be changed via `page_size` query parameter. The maximum allowed page size ATM is 100.


## Versioning

Example API uses date-based versioning, where version is given as part of the path in URL.
We release new version whenever a backwards-incompatible changes are made to the API.

E.g. if the client wants to use version `2018-02-21` then all API requests must use `/api/2018-02-21/` as path prefix.

We consider the following changes to be backwards-compatible:

- Adding new API resources.
- Adding new optional request parameters to existing API methods.
- Adding new properties to existing API responses.

Old versions might be removed approximately one year after they become deprecated.


### Version History

- **2018-02-21** - initial version


## Response codes and errors

Example API uses standard HTTP response codes to indicate the success or failure of an API request.
In general, codes in the 2xx range indicate success,
codes in the 4xx range indicate an error that failed given the information provided
(e.g., a required parameter was omitted, waybill couldn't be created, etc.),
and codes in the 5xx range indicate server-side errors (these are rare).

Error responses include body in JSON format, according to the JSON API spec.
Error response body always has `errors` key, containing information about the problems encountered.


### 400 Bad Request

Invalid data was submitted, e.g. when trying to create / update an object.

Example response body:

    :::json
    {
        "errors": [
            {
                "detail": "Company with this waybill prefix already exists.",
                "source": {
                    "pointer": "/data/attributes/waybill_prefix"
                },
                "status": "400"
            }
        ]
    }


### 401 Unauthorized

Requested resource requires authenticated user.

Example response body:

    :::json
    {
        "errors": [
            {
                "detail": "Authentication credentials were not provided.",
                "source": {
                    "pointer": "/data"
                },
                "status": "401"
            }
        ]
    }


### 403 Forbidden

Authenticated user does not have permission to access the given resource

Example response body:

    :::json
    {
        "errors": [
            {
                "detail": "You do not have permission to perform this action.",
                "source": {
                    "pointer": "/data"
                },
                "status": "403"
            }
        ]
    }


### 404 Not Found

Request object does not exist.

Example response body:

    :::json
    {
        "errors": [
            {
                "detail": "Not found.",
                "source": {
                    "pointer": "/data/attributes/detail"
                },
                "status": "404"
            }
        ]
    }

"""
