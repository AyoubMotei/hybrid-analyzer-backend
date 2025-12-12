from app.services.huggingface import classify_text


def test_hugging_face(mocker):
  
    fake_output = [
        
        {
            "label": "sport",
            "score": 0.93
        }
    ]

  
    fake = mocker.Mock()
    fake.status_code = 200
    fake.json.return_value = fake_output

    
    
    mocker.patch(
        "app.services.huggingface.requests.post",
        return_value=fake
    )

    category, score = classify_text(
        "L'équipe a dominé le match"
    )

    assert category == "sport"
    assert score == 0.93
