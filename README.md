# Usage

# Plugins

Plugins implement the following api:

  * variable `ids` - list to the standard identifiers used for stuttgart
  * function `get_data` - takes the list of ids and returns a list of entries and cfg dict

## `get_data()`

returns a list of data points for each id:

```
[
  {
    "_id": "<unique identity>",
    "_name": "<name of data source based on id>",
    "_source": "<source name>",
    "_ts": "<timestamp of the input values>",

    "field1": <value1 (float)>,
    ... ,
    "fieldX": <valueX (float)>
  }
  ...
]
```
`_name`,`_id` and `_source`, `_ts` have a special meaning,
the rest are essentially key value pairs of the measurements.

# Dev Mode

```sh
nix-shell
```
