# PyBifrost

A burning rainbow bridge between scripting languages.

## Sample I/O

```javascript
recv {"module": "numpy"}
send {"result": {"__oid__": 4336043000}}
recv {"oid": 4336043000, "method": "array", "params": [[1,2,3]]}
send {"result": {"__oid__": 140566653384336}}
recv {"oid": 140566653384336, "attr": "size"}
send {"result": 3}
```

## Copyright

Copyright (c) 2013 Ben Pringle

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this program except in compliance with the License. A copy of the License is
provided in LICENSE.txt.

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
