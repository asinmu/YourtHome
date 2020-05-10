from rest_framework import serializers

from .models import *
from drf_writable_nested.serializers import WritableNestedModelSerializer


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'type')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'room')


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ('id', 'floor')


class ConstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Construction
        fields = ('id', 'name')


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ('id', 'name')


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'name')


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'total_area', 'living_area')

    def validate_living_area(self, data):
        if data < 0:
            raise serializers.ValidationError("Жилая площадь не может быть отрицательной величиной!!!")
        return data

    def validate_total_area(self, data):

        if data < 0:
            raise serializers.ValidationError("Общая площадь не может быть отрицательной величиной!!!")
        return data


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name')


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name', 'country')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'region')


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name', 'city')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'country', 'region', 'city', 'district', 'street', 'house_number', 'latitude', 'longitude')


class Location2Serializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    region = serializers.StringRelatedField()
    city = serializers.CharField()
    district = serializers.CharField()

    class Meta:
        model = Location
        fields = ('id', 'country', 'region', 'city', 'district', 'street', 'house_number', 'latitude', 'longitude')


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = ('id', 'furniture', 'heat', 'gas', 'electricity', 'internet', 'phone', 'elevator', 'security',
                  'parking')


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'name')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'role', 'phone', 'name', 'surname')


class PrettyContactSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField()

    class Meta:
        model = Contact
        fields = ('id', 'role', 'phone', 'name', 'surname')


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    apartment = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'apartment', 'name_of_publication', 'text_of_publication', 'date_of_publication', 'owner')


class BookingSerializer(serializers.ModelSerializer):
    apartment = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'apartment', 'arrival_date', 'departure_date')

    def validate(self, data):
        if data['arrival_date'] > data['departure_date']:
            raise serializers.ValidationError("Дата заезда"
                                              " не может быть позже даты выезда!!!")
        return data


class PhotoDetailSerializer(serializers.ModelSerializer):
    apartment = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ApartmentImage
        fields = ('id', 'apartment', 'image',)


class ApartmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentImage
        fields = ('image', 'id')


class ObjectsInApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectsInApartment
        fields = ('name',)


class NearbyObjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NearbyObjects
        fields = ('name',)


class uploadSerializer(serializers.HyperlinkedModelSerializer):
    images = ApartmentImageSerializer(source='apartment_image', many=True, read_only=True)

    class Meta:
        model = ApartmentImage
        fields = ('images', 'image', 'id')

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        my_view = self.context['view']
        object_id = my_view.kwargs.get('pk')
        apartment = Apartment.objects.get(id=object_id)
        for image_data in images_data.values():
            ApartmentImage.objects.create(apartment=apartment, image=image_data)
        apartment.save()
        return apartment


class PrettyApartmentSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    owner = serializers.StringRelatedField()
    type = serializers.StringRelatedField()
    series = serializers.StringRelatedField()
    construction_type = serializers.StringRelatedField()
    state = serializers.StringRelatedField()
    currency = serializers.StringRelatedField()
    location = Location2Serializer()
    apartment_image = uploadSerializer(many=True, read_only=True)
    area = AreaSerializer()
    contact = PrettyContactSerializer()
    detail = DetailSerializer()
    comments = CommentSerializer(many=True, read_only=True)
    orders = BookingSerializer(many=True, read_only=True)

    class Meta:
        model = Apartment
        fields = (
            'id', 'type', 'room', 'nearby_objects', 'floor', 'storey', 'area', 'series', 'title',
            'construction_type',
            'state', 'status',
            'detail', 'objects_in_apartment', 'location', 'price', 'currency', 'another_price', 'preview_image',
            'description',
            'pub_date', 'apartment_image', 'contact', 'owner', 'comments', 'orders')


class ApartmentSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    location = LocationSerializer()
    apartment_image = uploadSerializer(many=True, read_only=True)
    area = AreaSerializer()
    contact = ContactSerializer()
    detail = DetailSerializer()
    comments = CommentSerializer(many=True, read_only=True)
    orders = BookingSerializer(many=True, read_only=True)
    floor = serializers.IntegerField()
    storey = serializers.IntegerField()

    class Meta:
        model = Apartment
        fields = ('id', 'type', 'room', 'floor', 'area', 'series', 'title', 'construction_type', 'state',
                  'detail', 'location', 'price', 'currency', 'another_price', 'preview_image',
                  'description', 'status',
                  'pub_date', 'storey', 'nearby_objects', 'objects_in_apartment', 'apartment_image', 'contact', 'owner',
                  'comments', 'orders')

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        area_data = validated_data.pop('area')
        contact_data = validated_data.pop('contact')
        detail_data = validated_data.pop('detail')

        area = Area.objects.create(**area_data)
        location = Location.objects.create(**location_data)
        contact = Contact.objects.create(**contact_data)
        detail = Detail.objects.create(**detail_data)
        apartment = Apartment.objects.create(area=area, location=location, detail=detail, contact=contact,
                                             **validated_data)

        return apartment

    def validate_floor(self, data):
        if data < 0:
            raise serializers.ValidationError("Этаж не может быть отрицательной величиной!!!")
        return data

    def validate_storey(self, data):
        if data < 0:
            raise serializers.ValidationError("Этажность не может быть отрицательной величиной!!!")
        return data

    def validate_price(self, data):
        if data < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной величиной!!!")
        return data


class ChangeApartmentSerializer(WritableNestedModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    location = LocationSerializer()
    apartment_image = ApartmentImageSerializer(many=True)
    area = AreaSerializer()
    contact = ContactSerializer()
    detail = DetailSerializer()
    comments = CommentSerializer(many=True, read_only=True)
    orders = BookingSerializer(many=True, read_only=True)
    floor = serializers.IntegerField()
    storey = serializers.IntegerField()

    class Meta:
        model = Apartment
        fields = ('id', 'type', 'room', 'floor', 'area', 'series', 'title', 'construction_type', 'state',
                  'detail', 'location', 'price', 'currency', 'another_price', 'preview_image',
                  'description',
                  'pub_date', 'storey', 'nearby_objects', 'objects_in_apartment', 'apartment_image', 'contact', 'owner',
                  'comments', 'orders')

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        area_data = validated_data.pop('area')
        contact_data = validated_data.pop('contact')
        detail_data = validated_data.pop('detail')

        area = Area.objects.create(**area_data)
        location = Location.objects.create(**location_data)
        contact = Contact.objects.create(**contact_data)
        detail = Detail.objects.create(**detail_data)
        apartment = Apartment.objects.create(area=area, location=location, detail=detail, contact=contact,
                                             **validated_data)

        return apartment

    def validate_floor(self, data):
        if data < 0:
            raise serializers.ValidationError("Этаж не может быть отрицательной величиной!!!")
        return data

    def validate_storey(self, data):
        if data < 0:
            raise serializers.ValidationError("Этажность не может быть отрицательной величиной!!!")
        return data

    def validate(self, data):
        floor = data.get('floor')
        storey = data.get('storey')
        area = data.get('area')
        existing_data = self.to_representation(self.instance)

        if floor and storey:
            if data['floor'] > data['storey']:
                raise serializers.ValidationError("Этаж не должен превышать этажность дома!!!")
        elif storey:
            if existing_data['floor'] > data['storey']:
                raise serializers.ValidationError("Этажность не может быть меньше этажа дома!!!")
        elif floor:
            if existing_data['storey'] < data['floor']:
                raise serializers.ValidationError("Этаж не должен превышать этажность дома!!!")
        if area:
            living_area = area.get('living_area')
            total_area = area.get('total_area')
            if total_area and living_area:
                if area['living_area'] > area['total_area']:
                    raise serializers.ValidationError("Жилая площадь не должна быть больше чем общая площадь!!!")
            elif total_area:
                if existing_data['area']['living_area'] < area['total_area']:
                    raise serializers.ValidationError("Общая площадь не может быть меньше жилой площади!!!")
            elif living_area:
                if existing_data['area']['total_area'] < area['living_area']:
                    raise serializers.ValidationError("Жилая площадь не должна быть больше чем общая площадь!!!")
        return data

    def validate_price(self, data):
        if data < 0:
            raise serializers.ValidationError("Цена не может " \
                                              "быть отрицательной величиной!!!")
        return data


class ApartmentsSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.__str__')
    location = Location2Serializer(many=False)
    apartment_image = uploadSerializer(many=True, read_only=True)
    contact = PrettyContactSerializer(many=False)
    type = serializers.CharField(source='type.__str__')
    room = serializers.IntegerField()
    currency = serializers.CharField(source='currency.__str__')
    floor = serializers.IntegerField()
    series = serializers.CharField(source='series.__str__')
    construction_type = serializers.CharField(source='construction_type.__str__')
    state = serializers.CharField(source='state.__str__')
    comments = CommentSerializer(many=True, read_only=True)
    orders = BookingSerializer(many=True, read_only=True)
    detail = DetailSerializer(many=False)
    area = AreaSerializer(many=False)

    class Meta:
        model = Apartment
        fields = ('id', 'type', 'room', 'title', 'floor', 'storey', 'area', 'series', 'construction_type', 'state',
                  'detail', 'nearby_objects', 'location', 'price', 'currency', 'another_price', 'preview_image',
                  'description',
                  'pub_date', 'apartment_image', 'objects_in_apartment', 'contact', 'owner', 'comments', 'orders')


class PhotoChangeSerializer(serializers.ModelSerializer):
    apartment = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ApartmentImage
        fields = ('id', 'apartment', 'image',)


class ChangeApartmentImageSerializer(serializers.ModelSerializer):
    apartment = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ApartmentImage
        fields = ('id', 'apartment', 'image',)


class FrontApartmentsSerializer(serializers.ModelSerializer):
    location = Location2Serializer(many=False)
    currency = serializers.CharField(source='currency.__str__')
    preview_photo = serializers.SerializerMethodField()
    owner = serializers.StringRelatedField()

    class Meta:
        model = Apartment
        fields = ('id', 'title', 'location', 'price', 'currency', 'another_price', 'preview_photo', 'owner')

    def get_preview_photo(self, obj):
        preview_photo = obj.apartment_image.first()
        serializer = uploadSerializer(preview_photo)
        return serializer.data
