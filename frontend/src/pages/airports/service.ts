import { fetchAPI } from "@/utils/request";

export async function getAirports(): Promise<any> {
  const url = '/api/airport/domestic-airports/';

  return fetchAPI({
    method: 'GET',
    url,
    authorization: true,
  });
}


export async function saveAirport(payload: any): Promise<any> {
  let url = `/api/airport/domestic-airports/`;

  url += payload.id ? `${payload.id}/` : '';

  return fetchAPI({
    method: payload.id ? 'PATCH' : 'POST',
    url,
    body: payload,
    authorization: true,
  });
}
