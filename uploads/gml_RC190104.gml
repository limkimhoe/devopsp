<?xml version="1.0" encoding="UTF-8"?>
<core:CityModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.opengis.net/citygml/2.0"
   xmlns:xAL="urn:oasis:names:tc:ciq:xsdschema:xAL:2.0" xmlns:xlink="http://www.w3.org/1999/xlink"
   xmlns:core="http://www.opengis.net/citygml/2.0"
   xmlns:gml="http://www.opengis.net/gml"
   xmlns:bldg="http://www.opengis.net/citygml/building/2.0"
   xmlns:app="http://www.opengis.net/citygml/appearance/2.0"
   xsi:schemaLocation="  http://www.opengis.net/citygml/2.0 http://schemas.opengis.net/citygml/2.0/cityGMLBase.xsd http://www.opengis.net/citygml/building/2.0 http://schemas.opengis.net/citygml/building/2.0/building.xsd http://www.opengis.net/citygml/appearance/2.0 http://schemas.opengis.net/citygml/appearance/2.0/appearance.xsd">
   <gml:description>3D City Model of Singapore</gml:description>
   <gml:name>RC190104</gml:name>
   <gml:boundedBy>
      <gml:Envelope srsDimension="3" srsName="urn:ogc:def:crs,crs:EPSG::3414,crs:EPSG::6916">
         <gml:lowerCorner>29475.868 31699.020 13.233</gml:lowerCorner>
         <gml:upperCorner>29485.544 31708.017 17.331</gml:upperCorner>
      </gml:Envelope>
   </gml:boundedBy>
   <core:cityObjectMember>
      <bldg:Building gml:id="SLA_BLDG2_c4070e91-bc1a-4422-a779-24f46191a2e3">
         <gml:name>1919</gml:name>
         <creationDate>2020-10-30</creationDate>
         <externalReference>
            <informationSystem>BCA Building ID</informationSystem>
            <externalObject>
               <name>A1553-00310-2011_2</name>
            </externalObject>
         </externalReference>
         <app:appearance>
         <app:Appearance>
         <app:theme>texturation</app:theme>
            <app:surfaceDataMember>
               <app:ParameterizedTexture>
               <app:imageURI>./tmaps/rc190104.tif</app:imageURI><app:mimeType>image/.TIF</app:mimeType>
               <app:wrapMode>none</app:wrapMode>
               <app:target uri="#poly_RC190104_p178_0">
                  <app:TexCoordList>
                     <app:textureCoordinates ring="#line_RC190104_p178_0">0.4486695 0.0000000 0.4486693 0.5875363 0.0031760 0.5875268 0.0031746 0.0000000 0.4486695 0.0000000</app:textureCoordinates>
                  </app:TexCoordList>
               </app:target>
               <app:target uri="#poly_RC190104_p178_1">
                  <app:TexCoordList>
                     <app:textureCoordinates ring="#line_RC190104_p178_1">0.1730004 0.9942964 0.0000000 0.9942964 0.0000000 0.6141732 0.1730004 0.6141732 0.1730004 0.9942964</app:textureCoordinates>
                  </app:TexCoordList>
               </app:target>
               <app:target uri="#poly_RC190104_p178_2">
                  <app:TexCoordList>
                     <app:textureCoordinates ring="#line_RC190104_p178_2">0.9967300 0.9942964 0.6713675 0.9942964 0.6713675 0.6141732 0.9967300 0.6141732 0.9967300 0.9942964</app:textureCoordinates>
                  </app:TexCoordList>
               </app:target>
               <app:target uri="#poly_RC190104_p178_3">
                  <app:TexCoordList>
                     <app:textureCoordinates ring="#line_RC190104_p178_3">0.6713675 0.9942964 0.4983642 0.9942964 0.4983642 0.6141732 0.6713675 0.6141732 0.6713675 0.9942964</app:textureCoordinates>
                  </app:TexCoordList>
               </app:target>
               <app:target uri="#poly_RC190104_p178_4">
                  <app:TexCoordList>
                     <app:textureCoordinates ring="#line_RC190104_p178_4">0.4983642 0.9942964 0.1730004 0.9942964 0.1730004 0.6141732 0.4983642 0.6141732 0.4983642 0.9942964</app:textureCoordinates>
                  </app:TexCoordList>
               </app:target>
               </app:ParameterizedTexture>
            </app:surfaceDataMember>
         </app:Appearance>
         </app:appearance>
         <bldg:class codeSpace="https://www.sla.gov.sg/qql/slot/u143/Newsroom/Circulars/CityGML/_AbstractBuilding_class.xml"></bldg:class>
         <bldg:function codeSpace="https://www.sla.gov.sg/qql/slot/u143/Newsroom/Circulars/CityGML/_AbstractBuilding_function.xml"></bldg:function>
         <bldg:usage codeSpace="https://www.sla.gov.sg/qql/slot/u143/Newsroom/Circulars/CityGML/_AbstractBuilding_usage.xml"></bldg:usage>
         <bldg:yearOfConstruction>2015</bldg:yearOfConstruction>
         <bldg:measuredHeight uom="meter">4.088</bldg:measuredHeight>
         <bldg:storeysAboveGround>1</bldg:storeysAboveGround>
         <bldg:consistsOfBuildingPart>
            <bldg:BuildingPart gml:id="PRC190104_1">
               <bldg:roofType codeSpace="https://www.sla.gov.sg/qql/slot/u143/Newsroom/Circulars/CityGML/_AbstractBuilding_roofType.xml">1000</bldg:roofType>
               <bldg:lod2Solid>
                  <gml:Solid gml:id="srf_RC190104_p1" srsName="urn:ogc:def:crs,crs:EPSG::3414,crs:EPSG::6916" srsDimension="3">
                  <gml:exterior>
                  <gml:CompositeSurface>
                     <gml:surfaceMember xlink:href="#os_RC190104_p178_0"/>
                     <gml:surfaceMember xlink:href="#os_RC190104_p178_1"/>
                     <gml:surfaceMember xlink:href="#os_RC190104_p178_2"/>
                     <gml:surfaceMember xlink:href="#os_RC190104_p178_3"/>
                     <gml:surfaceMember xlink:href="#os_RC190104_p178_4"/>
                     <gml:surfaceMember xlink:href="#os_RC190104_b_0"/>
                  </gml:CompositeSurface>
                  </gml:exterior>
                  </gml:Solid>
               </bldg:lod2Solid>
               <bldg:boundedBy>
                  <bldg:RoofSurface gml:id="roof_RC190104_p178_0">
                  <bldg:lod2MultiSurface>
                  <gml:MultiSurface>
                  <gml:surfaceMember>
                  <gml:OrientableSurface gml:id="os_RC190104_p178_0" orientation="+">
                  <gml:baseSurface>
                  <gml:Polygon gml:id="poly_RC190104_p178_0">
                  <gml:exterior>
                  <gml:LinearRing gml:id="line_RC190104_p178_0">
                  <gml:posList srsDimension="3">29482.68893162 31699.02198438 17.32571335 29485.54433297 31702.64658228 17.32070936 29478.72760919 31708.01661202 17.32589754 29475.87223020 31704.39209237 17.33090144 29482.68893162 31699.02198438 17.32571335 </gml:posList>
                  </gml:LinearRing>
                  </gml:exterior>
                  </gml:Polygon>
                  </gml:baseSurface>
                  </gml:OrientableSurface>
                  </gml:surfaceMember>
                  </gml:MultiSurface>
                  </bldg:lod2MultiSurface>
                  </bldg:RoofSurface>
               </bldg:boundedBy>
               <bldg:boundedBy>
                  <bldg:WallSurface gml:id="wall_RC190104_p178_1">
                  <bldg:lod2MultiSurface>
                  <gml:MultiSurface>
                  <gml:surfaceMember>
                  <gml:OrientableSurface gml:id="os_RC190104_p178_1" orientation="+">
                  <gml:baseSurface>
                  <gml:Polygon gml:id="poly_RC190104_p178_1">
                  <gml:exterior>
                  <gml:LinearRing gml:id="line_RC190104_p178_1">
                  <gml:posList srsDimension="3">29475.87223020 31704.39209237 17.33090144 29478.72760919 31708.01661202 17.32589754 29478.72294516 31708.01464510 13.23835259 29475.86756434 31704.39012311 13.24335649 29475.87223020 31704.39209237 17.33090144 </gml:posList>
                  </gml:LinearRing>
                  </gml:exterior>
                  </gml:Polygon>
                  </gml:baseSurface>
                  </gml:OrientableSurface>
                  </gml:surfaceMember>
                  </gml:MultiSurface>
                  </bldg:lod2MultiSurface>
                  </bldg:WallSurface>
               </bldg:boundedBy>
               <bldg:boundedBy>
                  <bldg:WallSurface gml:id="wall_RC190104_p178_2">
                  <bldg:lod2MultiSurface>
                  <gml:MultiSurface>
                  <gml:surfaceMember>
                  <gml:OrientableSurface gml:id="os_RC190104_p178_2" orientation="+">
                  <gml:baseSurface>
                  <gml:Polygon gml:id="poly_RC190104_p178_2">
                  <gml:exterior>
                  <gml:LinearRing gml:id="line_RC190104_p178_2">
                  <gml:posList srsDimension="3">29478.72760919 31708.01661202 17.32589754 29485.54433297 31702.64658228 17.32070936 29485.53967330 31702.64461190 13.23316441 29478.72294516 31708.01464510 13.23835259 29478.72760919 31708.01661202 17.32589754 </gml:posList>
                  </gml:LinearRing>
                  </gml:exterior>
                  </gml:Polygon>
                  </gml:baseSurface>
                  </gml:OrientableSurface>
                  </gml:surfaceMember>
                  </gml:MultiSurface>
                  </bldg:lod2MultiSurface>
                  </bldg:WallSurface>
               </bldg:boundedBy>
               <bldg:boundedBy>
                  <bldg:WallSurface gml:id="wall_RC190104_p178_3">
                  <bldg:lod2MultiSurface>
                  <gml:MultiSurface>
                  <gml:surfaceMember>
                  <gml:OrientableSurface gml:id="os_RC190104_p178_3" orientation="+">
                  <gml:baseSurface>
                  <gml:Polygon gml:id="poly_RC190104_p178_3">
                  <gml:exterior>
                  <gml:LinearRing gml:id="line_RC190104_p178_3">
                  <gml:posList srsDimension="3">29485.54433297 31702.64658228 17.32070936 29482.68893162 31699.02198438 17.32571335 29482.68427013 31699.02001165 13.23816839 29485.53967330 31702.64461190 13.23316441 29485.54433297 31702.64658228 17.32070936 </gml:posList>
                  </gml:LinearRing>
                  </gml:exterior>
                  </gml:Polygon>
                  </gml:baseSurface>
                  </gml:OrientableSurface>
                  </gml:surfaceMember>
                  </gml:MultiSurface>
                  </bldg:lod2MultiSurface>
                  </bldg:WallSurface>
               </bldg:boundedBy>
               <bldg:boundedBy>
                  <bldg:WallSurface gml:id="wall_RC190104_p178_4">
                  <bldg:lod2MultiSurface>
                  <gml:MultiSurface>
                  <gml:surfaceMember>
                  <gml:OrientableSurface gml:id="os_RC190104_p178_4" orientation="+">
                  <gml:baseSurface>
                  <gml:Polygon gml:id="poly_RC190104_p178_4">
                  <gml:exterior>
                  <gml:LinearRing gml:id="line_RC190104_p178_4">
                  <gml:posList srsDimension="3">29482.68893162 31699.02198438 17.32571335 29475.87223020 31704.39209237 17.33090144 29475.86756434 31704.39012311 13.24335649 29482.68427013 31699.02001165 13.23816839 29482.68893162 31699.02198438 17.32571335 </gml:posList>
                  </gml:LinearRing>
                  </gml:exterior>
                  </gml:Polygon>
                  </gml:baseSurface>
                  </gml:OrientableSurface>
                  </gml:surfaceMember>
                  </gml:MultiSurface>
                  </bldg:lod2MultiSurface>
                  </bldg:WallSurface>
               </bldg:boundedBy>
               <bldg:boundedBy>
                  <bldg:GroundSurface gml:id="gnd_RC190104_b_0">
                  <bldg:lod2MultiSurface>
                  <gml:MultiSurface>
                  <gml:surfaceMember>
                  <gml:OrientableSurface gml:id="os_RC190104_b_0" orientation="+">
                  <gml:baseSurface>
                  <gml:Polygon gml:id="poly_RC190104_b_0">
                  <gml:exterior>
                  <gml:LinearRing gml:id="line_RC190104_b_0">
                  <gml:posList srsDimension="3">29478.72294516 31708.01464510 13.23835259 29485.53967330 31702.64461190 13.23316441 29482.68427013 31699.02001165 13.23816839 29475.86756434 31704.39012311 13.24335649 29478.72294516 31708.01464510 13.23835259 </gml:posList>
                  </gml:LinearRing>
                  </gml:exterior>
                  </gml:Polygon>
                  </gml:baseSurface>
                  </gml:OrientableSurface>
                  </gml:surfaceMember>
                  </gml:MultiSurface>
                  </bldg:lod2MultiSurface>
                  </bldg:GroundSurface>
               </bldg:boundedBy>
            </bldg:BuildingPart>
         </bldg:consistsOfBuildingPart>
         <bldg:address>
            <Address>
               <xalAddress>
                  <xAL:AddressDetails>
                     <xAL:Country>
                        <xAL:CountryNameCode>SG</xAL:CountryNameCode>
                        <xAL:CountryName>Singapore</xAL:CountryName>
                        <xAL:Locality Type="Town">
                           <xAL:LocalityName>ROCHOR</xAL:LocalityName>
                           <xAL:Thoroughfare Type="Street">
                              <xAL:ThoroughfareNumber>110</xAL:ThoroughfareNumber>
                              <xAL:ThoroughfareName>SOPHIA ROAD</xAL:ThoroughfareName>
                           </xAL:Thoroughfare>
                           <xAL:PostalCode>
                              <xAL:PostalCodeNumber>228175</xAL:PostalCodeNumber>
                           </xAL:PostalCode>
                        </xAL:Locality>
                     </xAL:Country>
                  </xAL:AddressDetails>
               </xalAddress>
               <multiPoint>
                  <gml:MultiPoint srsName="urn:ogc:def:crs,crs:EPSG::3414,crs:EPSG::6916">
                     <gml:pointMember>
                        <gml:Point>
                           <gml:pos srsDimension="3">29480.704 31703.517 13.316</gml:pos>
                        </gml:Point>
                     </gml:pointMember>
                  </gml:MultiPoint>
               </multiPoint>
            </Address>
         </bldg:address>
      </bldg:Building>
   </core:cityObjectMember>
</core:CityModel>
