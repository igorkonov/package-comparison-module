import json



def get_dump_json(data: Any, filename: str) -> None:
    """
    A function to dump JSON data to a file.
    Parameters:
        data: The JSON data to be dumped.
        filename: The name of the file to dump the JSON data into.
    """
    if data:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False,
                default=lambda o: o.model_dump(),
            )

        log.success(f"Data saved to {filename}")
    else:
        log.error("No data available. No output file created.")
