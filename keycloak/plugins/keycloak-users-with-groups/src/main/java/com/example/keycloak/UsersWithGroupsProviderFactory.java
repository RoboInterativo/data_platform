package com.example.keycloak;

import org.keycloak.Config;
import org.keycloak.models.KeycloakSession;
import org.keycloak.models.KeycloakSessionFactory;
import org.keycloak.services.resource.RealmResourceProvider;
import org.keycloak.services.resource.RealmResourceProviderFactory;

public class UsersWithGroupsProviderFactory implements RealmResourceProviderFactory {

    @Override
    public String getId() {
        return "users-with-groups";
    }

    @Override
    public RealmResourceProvider create(KeycloakSession session) {
        return new UsersWithGroupsResource(session); // Непосредственно возвращаем ресурс
    }

    @Override
    public void init(Config.Scope config) {}

    @Override
    public void postInit(KeycloakSessionFactory factory) {}

    @Override
    public void close() {}
}
