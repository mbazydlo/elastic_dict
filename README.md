## Elastic Dict

Module provides ElasticDict class.
<p>It inherites from MutableMapping giving features of elastic access for keys and values.

### Init
Elastic key may be created in two ways:

- As empty init:
> ElasticDict()
>>ElasticDict[{}]

- As cast from dict:
> dict_ = {'foo': 'bar'}
> <p>ElasticDict(dict_)

>>ElasticDict[{'foo': 'bar'}]