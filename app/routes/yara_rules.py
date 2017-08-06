from app import app, db
from app.models import yara_rule
from flask import abort, jsonify, request
from flask.ext.login import current_user, login_required
from app.routes.tags_mapping import create_tags_mapping, delete_tags_mapping
import json


@app.route('/InquestKB/yara_rules', methods=['GET'])
@login_required
def get_all_yara_rules():
    entities = yara_rule.Yara_rule.query.all()
    return json.dumps([entity.to_dict() for entity in entities])


@app.route('/InquestKB/yara_rules/<int:id>', methods=['GET'])
@login_required
def get_yara_rule(id):
    entity = yara_rule.Yara_rule.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())


@app.route('/InquestKB/yara_rules', methods=['POST'])
@login_required
def create_yara_rule():
    entity = yara_rule.Yara_rule(
        state=request.json['state']['state']
        , name=request.json['name']
        , test_status=request.json['test_status']
        , confidence=request.json['confidence']
        , severity=request.json['severity']
        , description=request.json['description']
        , category=request.json['category']
        , file_type=request.json['file_type']
        , subcategory1=request.json['subcategory1']
        , subcategory2=request.json['subcategory2']
        , subcategory3=request.json['subcategory3']
        , reference_link=request.json['reference_link']
        , reference_text=request.json['reference_text']
        , condition=request.json['condition']
        , strings=request.json['strings']
        , created_user_id=current_user.id
        , modified_user_id=current_user.id
    )
    db.session.add(entity)
    db.session.commit()

    entity.tags = create_tags_mapping(entity.__tablename__, entity.id, request.json['tags'])

    return jsonify(entity.to_dict()), 201


@app.route('/InquestKB/yara_rules/<int:id>', methods=['PUT'])
@login_required
def update_yara_rule(id):
    entity = yara_rule.Yara_rule.query.get(id)
    if not entity:
        abort(404)
    entity = yara_rule.Yara_rule(
        state=request.json['state'],
        name=request.json['name'],
        test_status=request.json['test_status'],
        confidence=request.json['confidence'],
        severity=request.json['severity'],
        description=request.json['description'],
        category=request.json['category'],
        file_type=request.json['file_type'],
        subcategory1=request.json['subcategory1'],
        subcategory2=request.json['subcategory2'],
        subcategory3=request.json['subcategory3'],
        reference_link=request.json['reference_link'],
        reference_text=request.json['reference_text'],
        condition=request.json['condition'],
        strings=request.json['strings'],
        id=id,
        modified_user_id=current_user.id
    )
    db.session.merge(entity)
    db.session.commit()

    create_tags_mapping(entity.__tablename__, entity.id, request.json['addedTags'])
    delete_tags_mapping(entity.__tablename__, entity.id, request.json['removedTags'])

    return jsonify(entity.to_dict()), 200


@app.route('/InquestKB/yara_rules/<int:id>', methods=['DELETE'])
@login_required
def delete_yara_rule(id):
    entity = yara_rule.Yara_rule.query.get(id)
    tag_mapping_to_delete = entity.to_dict()['tags']

    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()

    delete_tags_mapping(entity.__tablename__, entity.id, tag_mapping_to_delete)

    return '', 204
