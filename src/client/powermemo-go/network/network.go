package network

import (
	"encoding/json"
	"net/http"
	
	mberror "github.com/memodb-io/powermemo/src/client/powermemo-go/error"
)

type BaseResponse struct {
	Data   map[string]interface{} `json:"data"`
	Errmsg string                 `json:"errmsg"`
	Errno  int                    `json:"errno"`
}

func UnpackResponse(resp *http.Response) (*BaseResponse, error) {
	if resp.StatusCode >= 400 {
		return nil, &mberror.ServerError{Message: resp.Status}
	}

	var baseResp BaseResponse
	if err := json.NewDecoder(resp.Body).Decode(&baseResp); err != nil {
		return nil, err
	}

	if baseResp.Errno != 0 {
		return nil, &mberror.ServerError{Message: baseResp.Errmsg}
	}

	return &baseResp, nil
} 