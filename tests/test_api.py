def test_upload_csv(client, sample_csv_bytes):
    response = client.post(
        "/upload", files={"file": ("sample_data.csv", sample_csv_bytes, "text/csv")}
    )
    body = response.json()
    assert response.status_code == 200
    assert body["rows"] == 6
    assert body["columns"] == 2
    assert isinstance(body["id"], int) and body["id"] > 0


def test_process_and_retrieve(client, uploaded_dataset_id, processing_body):
    response = client.post(
        f"/datasets/{uploaded_dataset_id}/process", json=processing_body
    )
    body = response.json()
    assert response.status_code == 200
    assert body["validation_rows_removed"] == 1
    assert body["cleaning_report"]["rows_before"] == 5
    assert body["cleaning_report"]["rows_after"] == 3

    response = client.get(f"/datasets/{uploaded_dataset_id}")
    body = response.json()
    assert response.status_code == 200
    assert body["total_rows"] == 3
    assert [r["student_id"] for r in body["data"]] == [1, 2, 5]
    assert [r["score"] for r in body["data"]] == [80, 90, 85]


def test_retrieve_missing_dataset(client):
    assert client.get("/datasets/999").status_code == 404