// noinspection BadExpressionStatementJS

(lat1, lon1, lat2, lon2, maxResults, headers) => {
  const baseUrl = 'https://app.parkmobile.io/api/zones/search'
  const parsedHeaders = typeof headers === 'string' ? JSON.parse(headers) : headers

  const parkingType = '1'
  let url = `${baseUrl}?parkingType=${parkingType}`
  url += `&upper=${lat1},${lon1}`
  url += `&lower=${lat2},${lon2}`
  if (maxResults)
    url += `&maxResults=${maxResults}`

  const req = fetch(url, {
    method: 'GET',
    mode: 'same-origin', // no-cors, *cors, same-origin
    credentials: 'same-origin', // include, *same-origin, omit
    headers: parsedHeaders,
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    // body: JSON.stringify(data) // body data type must match "Content-Type" header
  })

  console.log('New request: ', url, parsedHeaders, req)
  return req.then(resp => resp.json())
}
